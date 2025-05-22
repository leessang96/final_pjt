from django.shortcuts import render

import yfinance as yf
from django.http import JsonResponse

def gold_price(request):
    period = request.GET.get('period', '1mo')  # 기본값: 1개월
    gold = yf.Ticker("GC=F")
    hist = gold.history(period=period)

    # 날짜와 가격 리스트로 반환
    prices = [
        {"date": str(date.date()), "price": round(row["Close"], 2)}
        for date, row in hist.iterrows()
    ]

    return JsonResponse({"prices": prices})

def silver_price(request):
    period = request.GET.get('period', '1mo')  # 기본값: 1개월
    sliver = yf.Ticker("SI=F")
    hist = sliver.history(period=period)

    # 날짜와 가격 리스트로 반환
    prices = [
        {"date": str(date.date()), "price": round(row["Close"], 2)}
        for date, row in hist.iterrows()
    ]

    return JsonResponse({"prices": prices})