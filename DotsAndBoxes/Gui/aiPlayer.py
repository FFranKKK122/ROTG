from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import asyncio
import websockets
import json


if __name__ == "__main__":
    # 560 pixel 
    HEIGHT = 560
    WIDTH  = HEIGHT*0.9
    GRID_SIZE = 3 # 3*3 DotAndBox
    CELL_X_PIXEL = WIDTH // (GRID_SIZE + 2) -5
    CELL_Y_PIXEL = HEIGHT // (GRID_SIZE + 2) - 20

    # 選要哪一條邊
    def select( driver,canvas , x ,y):
        x_pixel , y_pixel = mapOrdinate(x , y)
        ActionChains(driver).move_to_element(canvas).move_by_offset(x_pixel , y_pixel).click().perform()

    # map Ordinate to Canvas pixel
    # x,y 必一奇一偶
    def mapOrdinate(x , y):
        # 懶得改 直接交換
        x , y = y , x
        if (x%2) == 0 :
            x = x//2 
            x = int((x+0.5)*CELL_X_PIXEL - WIDTH//2) +10
        else:
            x = (x+1)//2
            x = int((x)*CELL_X_PIXEL - WIDTH//2 ) +10
            
        if (y%2) == 0:
            y = y//2
            y = int((y+0.5)*CELL_Y_PIXEL - HEIGHT//2 ) +70
        else:
            y = (y+1)//2
            y = int((y)*CELL_Y_PIXEL - HEIGHT//2 ) + 70
        
        return x , y

    async def aiSelect():
        uri = "ws://localhost:8765"
        driver = webdriver.Chrome('C:/Users/MHLAB/Desktop/chromedriver') # 記得改
        driver.get("C:/Users/MHLAB/Desktop/啟發式/DotAndBoxGUI/game.html") #記得改
        canvas  = driver.find_element_by_xpath("//canvas[1]") 
        while True:
            async with websockets.connect(uri) as websocket:
                side = await websocket.recv()
                side = json.loads(side)
                print('Player Choose ',side['x'] , side['y'])

                # AI 要選哪一邊改這裡 目前讓電腦自動下 下面一條
                if(side['nextTurn'] == 'AI' ):
                    print('AI  Choose ' ,side['x']+2 , side['y'])
                    select(driver,canvas , side['x']+2 ,side['y'])

    
    asyncio.get_event_loop().run_until_complete(aiSelect())



    # for element in itertools.product([1,3,5,7],[2,4,6]):
    #     print(element)
    #     select(driver,canvas , element[0] , element[1])
    # for element in  itertools.product([2,4,6],[1,3,5,7]):
    #     print(element)
    #     select(driver,canvas , element[0] , element[1])
    # 107 ,126