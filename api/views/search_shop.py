import asyncio
import copy
import functools
from decimal import Decimal, ROUND_HALF_UP

import googlemaps
import requests
from bs4 import BeautifulSoup
from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Shop, Search, Place, Category
from api.serializer import ShopSerializer, SearchSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class SearchShop(generics.ListAPIView):
    serializer_class = SearchSerializer

    def get_queryset(self, **kwargs):
        try:
            queryset = Search.objects.get(place_code=kwargs['place_code'],
                                          category_code=kwargs['category_code'])
        except Search.DoesNotExist:
            return None

        return queryset

    def list(self, request, *args, **kwargs):
        try:
            search_query = self.get_search_query()
        except IncorrectSearchCodeException as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset(**search_query)

        if queryset is None or queryset.is_more_one_month():
            register = RegisterNewShop(search_query)
            register.get_tabelog_data()
            if len(register.shops) == 0:
                return Response({"message": "Shop not found"})
            register.get_google_data()
            register.register_new_data()
            queryset = self.get_queryset(**search_query)

        serializer = self.get_serializer(queryset)

        return Response(serializer.data)

    def get_search_query(self):
        if 'place' in self.request.query_params:
            place = self.request.query_params['place']
            if not Place.objects.filter(place_code=place).exists():
                raise IncorrectSearchCodeException('Incorrect place code')
        else:
            place = ''

        if 'category' in self.request.query_params:
            category = self.request.query_params['category']
            if not Category.objects.filter(category_code=category).exists():
                raise IncorrectSearchCodeException('Incorrect category code')
        else:
            category = ''

        return {'place_code': place, 'category_code': category}


class RegisterNewShop:
    def __init__(self, search_query):
        self.search_query = search_query
        self.shops = []
        self.google_maps_client = googlemaps.Client(key="AIzaSyCd6oVwry-gg8aEaUonAYL4xpVGXm1YjsY")

    def get_tabelog_data(self, page_num=3, limit=3):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # スクレイピング対象のURL生成
        urls = [
            f"{self.search_query['place_code']}/rstLst/{self.search_query['category_code']}/{page}/?SrtT=rt".replace(
                '//', '/') for page in range(1, page_num + 1)]
        urls = ['https://tabelog.com/' + url for url in urls]

        loop.run_until_complete(self._limited_parallel_call_tabelog(urls, limit))

    async def _limited_parallel_call_tabelog(self, urls, limit):
        # 並列数の制限
        sem = asyncio.Semaphore(limit)

        async def call(url):
            async with sem:
                return await self._scraping_tabelog(url)

        return await asyncio.gather(*[call(url) for url in urls])

    async def _scraping_tabelog(self, url):
        loop = asyncio.get_event_loop()

        try:
            res = await loop.run_in_executor(None, requests.get, url)
            res.raise_for_status()
        except requests.exceptions.RequestException:
            return

        soup = BeautifulSoup(res.text, "html.parser")

        # 検索結果なし
        if soup.find("div", class_="rstlist-notfound"):
            return

        for element in soup.find_all("div", class_="list-rst"):
            name_element = element.find("a", class_="list-rst__rst-name-target")
            tabelog_rating_element = element.find("span", class_="list-rst__rating-val")
            tabelog_review_num_element = element.find("em", class_="list-rst__rvw-count-num")
            img_src_element = element.find("img", class_="cpy-main-image")

            try:
                name = name_element.text
                tabelog_rating = float(tabelog_rating_element.text)
                tabelog_review_num = int(tabelog_review_num_element.text)
                shop_url = name_element.get('href')
                img_src = img_src_element.get('data-original')
            except:
                continue

            self.shops.append(
                {'name': name, 'tabelog_rating': tabelog_rating, 'tabelog_review_num': tabelog_review_num,
                 'url': shop_url, 'img_src': img_src})

    def get_google_data(self, limit=60):

        for shop in copy.deepcopy(self.shops):
            search_shop = Shop.objects.filter(url=shop['url']).first()
            # すでに店舗が登録済みで一ヶ月以内に更新がある場合 検索対象から外す
            if search_shop is not None and not search_shop.is_more_one_month():
                new_search, _ = Search.objects.get_or_create(place_code=self.search_query['place_code'],
                                                             category_code=self.search_query['category_code'])
                new_search.shops.add(search_shop)
                self.shops.remove(shop)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._limited_parallel_call_google(limit))

    async def _limited_parallel_call_google(self, limit):
        # 並列数の制限
        sem = asyncio.Semaphore(limit)

        async def call(shop):
            async with sem:
                return await self._request_google_places(shop)

        return await asyncio.gather(*[call(shop) for shop in self.shops])

    async def _request_google_places(self, shop):
        loop = asyncio.get_event_loop()
        func = functools.partial(self.google_maps_client.places, shop['name'], language='ja')
        result = await loop.run_in_executor(None, func)

        # 情報が不足している場合は店舗情報を削除
        try:
            google_rating = result['results'][0]['rating']
            google_review_num = result['results'][0]['user_ratings_total']
            address = result['results'][0]['formatted_address']
        except:
            self.shops.remove(shop)
            return

        shop['google_rating'] = google_rating
        shop['google_review_num'] = google_review_num
        shop['address'] = address

    def register_new_data(self):
        if len(self.shops) == 0:
            return

        created_shops = []
        for shop in self.shops:
            total_rating = (shop['tabelog_rating'] + shop['google_rating'] * 2) / 3
            total_rating = float(Decimal(total_rating).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
            created_shops.append(Shop.objects.create(name=shop['name'], img_src=shop['img_src'], url=shop['url'],
                                                     address=shop['address'],
                                                     google_rating=shop['google_rating'],
                                                     google_review_num=shop['google_review_num'],
                                                     tabelog_rating=shop['tabelog_rating'],
                                                     tabelog_review_num=shop['tabelog_review_num'],
                                                     total_rating=total_rating))

        new_search, _ = Search.objects.get_or_create(place_code=self.search_query['place_code'],
                                                     category_code=self.search_query['category_code'])
        new_search.shops.add(*created_shops)


class IncorrectSearchCodeException(Exception):
    pass
