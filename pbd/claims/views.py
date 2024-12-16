# views.py
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import pandas as pd
import os
import aiofiles
import asyncio
import io
import plotly.express as px
import plotly.io as pio
import requests

# Global variable to cache the DataFrame and a lock for thread safety
df_cache = None
df_lock = asyncio.Lock()

async def load_csv():
    global df_cache
    async with df_lock:
        if df_cache is None:
            csv_path = os.path.join(settings.BASE_DIR, 'claims', 'Claims.csv')
            async with aiofiles.open(csv_path, mode='r') as f:
                content = await f.read()
                df_cache = pd.read_csv(io.StringIO(content))
                date_columns = [
                    'claim_received_date', 'claim_loss_date', 'claim_finalised_date',
                    'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time',
                    'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time', 'update_date'
                ]
                for col in date_columns:
                    if col in df_cache.columns:
                        df_cache[col] = pd.to_datetime(df_cache[col], errors='coerce').dt.date
    return df_cache

@csrf_exempt
async def fetch_claims_data(request):
    try:
        # Check if data is in cache
        data = cache.get('claims_data')
        if not data:
            df = (await load_csv()).copy()

            # Apply filters from request
            filters = request.GET
            if 'claim_numbers' in filters:
                claim_numbers = filters.get('claim_numbers').split(',')
                df = df[df['claim_number'].astype(str).isin(claim_numbers)]

            for col in ['source_system', 'general_nature_of_loss', 'line_of_business', 'claim_status', 'fault_rating', 'fault_categorisation']:
                if col in filters:
                    values = filters.get(col).split(',')
                    df = df[df[col].isin(values)]

            date_columns = [
                'claim_received_date', 'claim_loss_date', 'claim_finalised_date',
                'original_verified_date_of_loss_time', 'last_verified_date_of_loss_time',
                'catastrophe_valid_from_date_time', 'catastrophe_valid_to_date_time', 'update_date'
            ]
            for col in date_columns:
                if f"{col}_start" in filters and f"{col}_end" in filters:
                    start_date = filters.get(f"{col}_start")
                    end_date = filters.get(f"{col}_end")
                    df = df[df[col].between(start_date, end_date)]

            # Perform calculations
            total_claims = df["claim_number"].nunique()
            claims_monitored = 3071
            claims_with_leakage_opportunity = 1854
            leakage_opportunity_percentage = 60
            potential_leakage = 51200000
            leakage_rate_percentage = 100
            opportunities_not_actioned = 3063

            status_counts = df['claim_status'].value_counts().reset_index()
            status_counts.columns = ['claim_status', 'count']

            claims_over_time = df.groupby('claim_received_date').size().reset_index(name='claim_count')

            line_of_business_counts = df['line_of_business'].value_counts().reset_index()
            line_of_business_counts.columns = ['line_of_business', 'count']

            df['claim_received_date'] = pd.to_datetime(df['claim_received_date'], errors='coerce')
            df['month_year'] = df['claim_received_date'].dt.to_period('M').astype(str)
            monthly_status_counts = df.groupby(['month_year', 'claim_status']).size().reset_index(name='count')

            data = {
                'total_claims': total_claims,
                'claims_monitored': claims_monitored,
                'claims_with_leakage_opportunity': claims_with_leakage_opportunity,
                'leakage_opportunity_percentage': leakage_opportunity_percentage,
                'potential_leakage': potential_leakage,
                'leakage_rate_percentage': leakage_rate_percentage,
                'opportunities_not_actioned': opportunities_not_actioned,
                'status_counts': status_counts.to_dict(orient='records'),
                'claims_over_time': claims_over_time.to_dict(orient='records'),
                'line_of_business_counts': line_of_business_counts.to_dict(orient='records'),
                'monthly_status_counts': monthly_status_counts.to_dict(orient='records'),
                'filtered_data': df.head(20).to_dict(orient='records')
            }

            # Store data in cache for 24 hours (86400 seconds)
            cache.set('claims_data', data, timeout=86400)

        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

async def fetch_data():
    url = "http://localhost:8000/api/fetch_claims_data/"
    response = await requests.get(url)
    return response.json()

async def generate_graphs(request):
    # Check if graphs are in cache
    graphs = cache.get('graphs')
    if not graphs:
        data = fetch_data()
        if data:
            status_counts = pd.DataFrame(data["status_counts"])
            fig_status = px.bar(status_counts, x='claim_status', y='count', title="Claims by Status", color='claim_status')
            fig_status_json = fig_status.to_json()

            claims_over_time = pd.DataFrame(data["claims_over_time"])
            fig_time = px.line(claims_over_time, x='claim_received_date', y='claim_count', title="Claims Over Time")
            fig_time_json = fig_time.to_json()

            fig_pie = px.pie(status_counts, names='claim_status', title="Claim Status Distribution", hole=0.3)
            fig_pie_json = fig_pie.to_json()

            line_of_business_counts = pd.DataFrame(data["line_of_business_counts"])
            fig_line_of_business = px.bar(line_of_business_counts, y='line_of_business', x='count', orientation='h', title="Claims by Line of Business")
            fig_line_of_business_json = fig_line_of_business.to_json()

            monthly_status_counts = pd.DataFrame(data["monthly_status_counts"])
            fig_trend_monthly = px.bar(monthly_status_counts, x='month_year', y='count', color='claim_status', title="Monthly Claim Status Trend (Open vs Closed)", barmode='group')
            fig_trend_monthly_json = fig_trend_monthly.to_json()

            graphs = {
                'fig_status_json': fig_status_json,
                'fig_time_json': fig_time_json,
                'fig_pie_json': fig_pie_json,
                'fig_line_of_business_json': fig_line_of_business_json,
                'fig_trend_monthly_json': fig_trend_monthly_json,
            }

            # Store graphs in cache for 24 hours (86400 seconds)
            cache.set('graphs', graphs, timeout=86400)
    return JsonResponse(graphs)
