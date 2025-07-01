from django.shortcuts import render
from vnstock import Vnstock
from datetime import datetime, timedelta



import plotly.offline as opy
import plotly.graph_objs as go

def index(request):
    symbol = request.GET.get('symbol', 'TCB')
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not start or not end:
        end = datetime.now().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    stock = Vnstock().stock(symbol=symbol, source='VCI')
    df = stock.quote.history(start=start, end=end, interval='1D')
    plot_div = None
    if df is not None and not df.empty:
        df = df.sort_values('time', ascending=True)
        data = df.to_dict(orient='records')
        trace_close = go.Scatter(
            x=df['time'], y=df['close'], mode='lines+markers', name='Close',
            hovertemplate='Date: %{x}<br>Close: %{y}<extra></extra>'
        )
        trace_open = go.Scatter(
            x=df['time'], y=df['open'], mode='lines+markers', name='Open', opacity=0.5,
            hovertemplate='Date: %{x}<br>Open: %{y}<extra></extra>'
        )
        layout = go.Layout(
            title=f'{symbol} Price History',
            xaxis={'title': 'Date', 'automargin': True, 'side': 'bottom', 'anchor': 'y'},
            yaxis={'title': 'Price', 'automargin': True},
            margin=dict(l=0, r=0, t=60, b=80),
            hovermode='x unified',
            width=1300,
            height=600
        )
        fig = go.Figure(data=[trace_close, trace_open], layout=layout)
        plot_div = opy.plot(fig, auto_open=False, output_type='div')
    else:
        data = []
        plot_div = None
    start_raw = start  # yyyy-mm-dd format for input type="date"
    end_raw = end  # yyyy-mm-dd format for input type="date"
    start_formatted = datetime.strptime(start, '%Y-%m-%d').strftime('%d/%m/%Y')
    end_formatted = datetime.strptime(end, '%Y-%m-%d').strftime('%d/%m/%Y')
    return render(request, 'index.html', { 'data': data, 'symbol': symbol, 'start': start_formatted, 'end': end_formatted, 'start_raw': start_raw, 'end_raw': end_raw, 'plot_div': plot_div })
