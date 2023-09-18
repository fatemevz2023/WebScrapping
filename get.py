from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




'''
در  کلاس زیر به صورت پیش فرض مقادیر مورد نیاز درایور اجرا می شود و 
 مقداری که میخواهد سرچ شود و تعدادی محصولی که 
  میخواهد دریافت کند را تعیین کرد که بصورت پیش فرض 50 عدد تعریف شده است (find_prosuct) در متد 
'''

'''
(load_element) در متد
مقدار دریافت شده ارسال می شوند به تابع و مقدار لینک ها و تصاویر و قیمت و عنوان جدا و دریافت می شوند 
و به صورت زیپ شده برگردادنده می شوند 

'''
class load_data():
    def __init__(self,path_dirver):
        self.path=path_dirver 
        op = webdriver.ChromeOptions()
        op.add_argument("----window-size=1920,1080")
        op.add_argument("--headless")
        self.driver=webdriver.Chrome(executable_path=self.path,chrome_options=op)

    def find_product(self,text_search,number=50):
        self.text_search=text_search
        self.number=number
        self.driver.get(f'https://www.digikala.com/search/?q={self.text_search}')
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((
        By.CLASS_NAME,'product-list_ProductList__item__LiiNI')))
        time.sleep(3)
        prduct_count=self.driver.find_element(By.CSS_SELECTOR,".color-500.text-no-wrap.text-body-2.ellispis-1.d-flex-xl.ai-center.gap-2")
        prduct_count=prduct_count.get_attribute("innerHTML").split(" ")

        if prduct_count[0].find(",")!=-1:
            prduct_count=prduct_count[0].split(",")
            prduct_count="".join(prduct_count)
            prduct_count=int(prduct_count)
        else:
            prduct_count=int(prduct_count[0])

        if prduct_count<50:
            self.number=prduct_count
        scroll_num=500
        items=""
        
        while len(items)<self.number:
            if  len(items)!=22 or len(items)!=42:
                self.driver.execute_script(f'window.scrollTo(0,{scroll_num})')
                time.sleep(3)
                items=self.driver.find_elements(By.CLASS_NAME,"product-list_ProductList__item__LiiNI")
                scroll_num+=2000
            else:
                 time.sleep(3)
                 continue
        while len(items)>self.number:
            items.pop()
        return items

    def load_element(self,items):
        self.items=items
        links=[]
        images=[]
        prices=[]
        subjects=[]
        for item in self.items:
            link=item.find_element(By.TAG_NAME,"a")
            link=link.get_attribute("href")
            links.append(link)

            img=item.find_element(By.CSS_SELECTOR,".w-100.radius-medium.d-inline-block.lazyloaded")
            img=img.get_attribute("src")
            images.append(img)
            
            try:
                prc=item.find_element(By.CSS_SELECTOR,".d-flex.ai-center.jc-end.gap-1.color-700.color-400.text-h5.grow-1")
                prc=prc.find_element(By.TAG_NAME,"span")
                prc=prc.get_attribute("innerHTML")
                prices.append(prc)
            except:
               prc="ناموجود"
               prices.append(prc)
            
            sub=item.find_element(By.TAG_NAME,"h3")
            sub=sub.get_attribute("innerHTML")
            subjects.append(sub)
            
        return zip(links,images,prices,subjects)

if __name__=="__main__":
    path_dirver='assets/chromedriver.exe'
    text_search="کتاب اثر مرکب"
    loadProduct=load_data(path_dirver)
    product_elm=loadProduct.find_product(text_search)
    product_items=loadProduct.load_element(product_elm)
    with open('data.txt','w',encoding='utf-8') as f:
        for item in product_items:
            f.write(f"{item}\n")









