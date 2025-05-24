from django.shortcuts import render

from django.http import JsonResponse
import yfinance as yf
from datetime import datetime, timedelta


# 공통 로직
def fetch_price_data(ticker, start=None, end=None, period='1mo'):
    if end:
        try:
            end_dt = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
            end = end_dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    
    yf_ticker = yf.Ticker(ticker)
    if start and end:
        hist = yf_ticker.history(start=start, end=end)
    else:
        hist = yf_ticker.history(period=period)

    prices = [
        {"date": str(date.date()), "price": round(row["Close"], 2)}
        for date, row in hist.iterrows()
    ]

    return {"prices": prices}


# 금 가격
def gold_price(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period', '1mo')
    data = fetch_price_data("GC=F", start, end, period)
    return JsonResponse(data)


# 은 가격
def silver_price(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period', '1mo')
    data = fetch_price_data("SI=F", start, end, period)
    return JsonResponse(data)

# 구리 가격
def copper_price(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period', '1mo')
    data = fetch_price_data("HG=F", start, end, period)
    return JsonResponse(data)

# 원유 가격
def oil_price(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period', '1mo')
    data = fetch_price_data("CL=F", start, end, period)
    return JsonResponse(data)

# 천연가스 가격
def gas_price(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    period = request.GET.get('period', '1mo')
    data = fetch_price_data("NG=F", start, end, period)
    return JsonResponse(data)
