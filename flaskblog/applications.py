import pandas as pd
import numpy
import openpyxl
import xlrd
import xlwt
import xlsxwriter
from flaskblog import datetime


def securityapp(file):
    
    start = datetime.strptime('05:15:00', '%H:%M:%S').time()
            end = datetime.strptime('11:45:00', '%H:%M:%S').time()

            files = request.files.getlist('securityfileinputFile[]')
            #os.chdir('/Users/mobile/Dropbox/BACK OFFICE SECURITY FILE/')
            #print(os.getcwd())
            #FileList = glob.glob('*.rtf')
            #print(FileList)

            newdf = []

            for file in files:
                inputfilename = file
                excel_file = inputfilename
                store_number = file
                a = str(store_number)
                print(a)
                b = re.search('\d+', a).group()
                print(b)
                print(store_number)

                df = pd.read_csv(excel_file, sep='\t', header=None)
                df.columns = ['Text']
                print(df.dtypes)
                print(df.head)

                df2 = df[df['Text'].str.contains('Pump', na=False)].copy()
                print(df2)

                if df2.empty:
                    continue

                df2['Time'] = df2['Text'].str.extract('(..:..:..)', expand=True)
                df2['Time'] = pd.to_datetime(
                    df2['Time'], format='%H:%M:%S').dt.time
                df2 = df2[df2['Time'].between(start, end)]

                df2['Date'] = df2['Text'].str.slice(start=0, stop=9)
                df2['Date'] = pd.to_datetime(
                    df2['Date'], format='%d %b %y').dt.date
                #df2['Date']=df2['Date'].datetime.strptime(b1, "%d %m %y").strftime("%b-%Y")

                df2['Store'] = b
                print(df2)
                newdf.append(df2)

            newdf = pd.concat(newdf)

            #newdf.to_excel("Pumps to Prepay" + ".xlsx", engine='xlsxwriter')
            #print(newdf.dtypes)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        newdf.to_excel(writer)
        writer.save()
        output.seek(0)
