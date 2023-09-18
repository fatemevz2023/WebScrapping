from dash import Dash,dcc , Output, Input,State
import dash_bootstrap_components as dbc
import dash_html_components as html
import os
import plotly.graph_objects as go 
import get

#start driver from file get.py
path_dirver='assets/chromedriver.exe'
loadProduct=get.load_data(path_dirver)

#start dash
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.append_css({"external_url": "/assets/styles.css"})
title = html.H2('دنبال چی می گردی؟')
subtitle = html.P('با کالو هر کالایی رو که بخوای پیدا می کنی. فقط کافیه یه اسم بدی!', style={'text-align':'center', 'direction':'rtl'})
tBox = dcc.Input(
    id='searchname',
    value='',
    placeholder=' جستجو  ...',
    type='text',
    style={
        'width': '50%',
        'color': '#8d8d8d',
        'margin-bottom': '10px',
        'direction': 'rtl',
        'padding': '10px 20px',
        'border': '1px solid #ddd',
        'border-radius': '25px',
    }
)

btn = html.Button(
    id='submit-button',
    children='جستجو',
    style={
        'background-color': '#03a9f4',
        'color': '#fff',
        'border-radius': '25px',
        'padding': '10px 20px',
        'border': '1px solid #ddd',
        'margin-bottom': '10px',
        'font-weight': 'bold'
    }
)

# Navigation bar
navbar = html.Header(className="header", children=[
        html.Div(className="container", children=[
            html.Section(className="section1", children=[
                html.Img(className="logo-header", src="/assets/Logo.png", alt="kalo-img"),
                html.Ul(className="menu", children=[
                    html.Li(className="menu-item", children=[
                        html.A(className="menu-item__link", children="تماس با ما", href="#")
                    ]),
                    html.Li(className="menu-item", children=[
                        html.A(className="menu-item__link", children="درباره کالو", href="#")
                    ])
                ])
            ])
        ])
    ])



# sample Data for products
'''
products = [
    
    {"name": "Product 1", "image": "/assets/image1.png", "price": "$10.00"},
    {"name": "Product 2", "image": "/assets/image2.png", "price": "$20.00"},
    {"name": "Product 3", "image": "/assets/image3.png", "price": "$30.00"},
    {"name": "Product 4", "image": "/assets/image1.png", "price": "$10.00"},
    {"name": "Product 5", "image": "/assets/image2.png", "price": "$20.00"},
    {"name": "Product 6", "image": "/assets/image3.png", "price": "$30.00"},
    
]
'''
#  تابع برای زمانی کال بک ها اجرا برگشت داده می شود و
#  این  تابع اجرا شده و داده ها داخل لایه ها دش ریخته می شود
def prdc(list_items):
    products=[]
    #file=open("assets/data.txt", "r",encoding='utf-8')
    cnt=1
    #with file as f:
    for item in list_items:
        #item=eval(item)
        data_product={"name": f"{item[3]}", "image": f"{item[1]}", "price":  f"{item[2]}","link": f"{item[0]}","c":cnt}
        products.append(data_product)
        cnt+=1

    # Create card for each product

    cards = []
    for product in products:
        card =dbc.Col([dbc.Card(
            [
                html.A(href=product["link"],target="_blank",
                    children=[html.Img(src=product["image"]),
                dbc.CardBody(
                    [
                        html.Div(product["c"], className="abs"),
                        html.H5(product["name"], className="card-title"),
                        html.P(f'{product["price"]} تومان', className="card-text"),
                    ]
                )])
            ],
            style={"width": "18rem",
                   "position":"relative",
                    'background-color': '#fff',
                    "margin":"35px"},
        
        )],sm=4)
        cards.append(card)
        #file.close()

    # Create columns to hold the cards
    row1 = dbc.Row(cards[:3])
    row2 = dbc.Row(cards[3:6])
    row3 = dbc.Row(cards[6:])

    # Create a row to hold the columns
    productbox = dbc.Row([row1, row2, row3] , className="productbox")
    return productbox



my_graph = dcc.Graph(figure={}) #گراف 
prd=html.Div() # بخش اصلی نگه دارنده محصولات
my_btn = dbc.Button('نمایش نمودار',style={'margin-top':'20px'}) #دکمه


@app.callback(
    Output(my_graph,component_property='figure'),
    Output(prd,component_property='children'),
    Output(btn,component_property='n_clicks'),
    [Input('submit-button', 'n_clicks')],
    [State('searchname', 'value')],
)
def show_images(n_clicks,text_search):
    if n_clicks:
        try:
            # get data from methods in file get.py
            product_elm=loadProduct.find_product(text_search)
            product_items=loadProduct.load_element(product_elm)

            #write in file data
            list_items=[]
            list_prc=[]
            #file_data=open('assets/data.txt','w',encoding='utf-8')
            #with file_data as f:
            for item in product_items:
                #f.write(f"{item}\n")
                list_items.append(item)
                if item[2]=="ناموجود":
                    prc=0
                    list_prc.append(prc)
                else:
                    prc=item[2].split(",")
                    prc="".join(prc)
                    prc=int(prc)
                    list_prc.append(prc)
            
            #graph
            figure = go.Figure(data=go.Scatter(x=list(range(1,len(list_prc)+1)), y=list_prc))
            figure.update_yaxes(tickformat=".0f")
            
            #file_data.close()

            # اجرای تابع جهت خواندن اطلاعات از فایل تکست دیتا و درون ریزی اطلاعات داخل لایه های دش
            children=prdc(list_items)
        except:
            children=html.Div(className="error",children=[html.P("عملیات با خطا مواجه شد. از اتصال به اینترنت مطمئن شوید و یا مجددا امتحان کنید")])
            figure=""
        return figure,children,n_clicks
    

app.layout = dbc.Row(className="", children=[ 
dbc.Row(className="background", children=[
    navbar, # منوی بالا
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([title], width=12)
    ]), #تیتر اصلی صفحه
    dbc.Row([
        dbc.Col([subtitle], width=12)
    ]),#عنوان فرعی صفحه
    dbc.Row([
        dbc.Col([tBox], width={"size": 12, "offset": 12}, className="text-center justify-content-center"),
        dbc.Col([btn], width={"size": 6, "offset": 3}, className="text-center justify-content-center")
    ]),
    html.Br()]),
    prd, # محصولات
    html.H2('نمودار قیمت',style={'text-align':'center','margin-top':'20px','border-top-color':'#80808038','border-top-width':'0.5px','border-top-style':'solid'}),
    dbc.Row([my_graph],className='text-center'), #نمودار
    html.Br()
])

if __name__=='__main__':
    app.run_server(port='8000')
