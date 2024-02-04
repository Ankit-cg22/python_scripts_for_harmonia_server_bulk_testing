import pandas as pd
import aiohttp
import asyncio
import httpx
from openpyxl import load_workbook
from datetime import datetime
import json 

async def fetch_data(session, url, data=None):
    async with session.post(url, data=data) as response:
        return await response.text()


async def async_post_request_bplus(url, data):
    async with httpx.AsyncClient() as client:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = await client.post(url, data=json.dumps(data), headers=headers)
        if(response.status_code==200):
            response_data= response.json()
            x,y = response_data.values()
            z = int(y)
            return y
        else:
            return 0

async def async_post_request_harmonia(url, data):
    async with httpx.AsyncClient() as client:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = await client.post(url, data=json.dumps(data), headers=headers)
        #print("awaiting response text harmonia")
        if(response.status_code==200):
            response_data= response.json()
            x,y = response_data.values()
            a,b = y.values()
            z = int(b)
            return z
        else:
            return 0



async def process_query(session,index, row,df):
    key = row['Key']
    value=row['Value']
    query_url_bplus = "https://bplus.adaptable.app/insert"
    data = {"key": key, "value": value}
   
    query_url_harmonia ="https://harmonia-b-plus-tree-server.onrender.com/insert"

    if pd.notna(query_url_bplus and query_url_harmonia):  # Check if the URL is not empty
        response_time = await async_post_request_bplus( query_url_bplus, data)
        response_time2 = await async_post_request_harmonia(query_url_harmonia, data)
        # Update the DataFrame with the response time
        df.at[index, 'Harmonia'] = response_time2
        df.at[index, 'BPLUS'] = response_time
       

async def main():
    input_file_path = 'insert_input.xlsx'
    df = pd.read_excel(input_file_path)    
    df['Harmonia'] = None
    df['BPLUS'] = None
    

    async with aiohttp.ClientSession() as session:
        tasks = [process_query(session, index, row,df) for index, row in df.iterrows()]
        await asyncio.gather(*tasks)


    output_file_path = 'output_results.xlsx'
    with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
        #writer.book = load_workbook(output_file_path)
        df.to_excel(writer, sheet_name='Sheet1', index=False)

   

if __name__ == '__main__':
    asyncio.run(main())
