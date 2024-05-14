#reading the dataframe
import pandas as pd
print('Enter the drive')
drive = input()
print('Enter the folder name:')
folder= input()
str_folder = str(folder)+'_without_result'+'.csv'
df_save=pd.read_csv(str_folder)
#Indexing each node
import pandas as pd
for count in range(len(df_save)):
    inp_dir =count
    path = ''''''+str(drive.upper()) +''':\\'''+str(folder)+'\\'+str(inp_dir)+'/'
    directory = ''''''+str(drive.upper()) +''':\\'''+str(folder)+'\\'
#     path = 'E:\\ansys\\'+str(inp_dir)+'/'
#     os.mkdir(path)
    #with open('E:\\ansys\\'+str(inp_dir)+'/nodeindex.txt','a+') as file1:
    file1 = open(path+'nodeindex.txt', 'r')
    Lines = file1.readlines()
    df = pd.DataFrame(columns=['node','x','y','z'])
    for i in Lines:
      out =i.split()
      if "-" in out[0]:
        j=out[0].split("-")
        out.pop(0)
        k =j[1]+'-'+j[2]
        j.pop(1)
        j.pop(1)
        j.insert(1,k)
        out.insert(0,j[0])
        out.insert(1,j[1])
      if len(out)==4:
        df = df.append(pd.Series(out, index=df.columns), ignore_index=True)
      elif len(out)==3:
        out.insert(3,0)
        df = df.append(pd.Series(out, index=df.columns), ignore_index=True)
    #converting object type into float
    df['x'] = df['x'].astype(float)
    df['y'] = df['y'].astype(float)
    df['z'] = df['z'].astype(float)
    #Scrapping
    df.loc[df['x']<10**-5, 'x']=0
    #Indexing 
    list_z,list_y,list_zx,list_zy = [],[],[],[]
    index =[]
    for i in range(len(df['x'])):
            if df['x'][i] == 0:
              list_z.append(df['z'][i])
              list_y.append(df['y'][i]) 
            else:
              if df['z'][i] == 0:
                list_zx.append(df['x'][i])
                list_zy.append(df['y'][i])
    list_z.sort()
    list_y.sort()
    list_zx.sort()
    list_zy.sort()
    for i in range(len(df['z'])):
      if df['z'][i] == list_z[-1]: index.append('a')
      elif df['z'][i] == list_z[-2]: index.append('b')
      elif df['z'][i] == list_z[-3]: index.append('c')
      else: 
          if df['y'][i]==list_y[-1]: index.append('d')
          elif df['y'][i]==list_y[-2]: index.append('e')
          elif df['y'][i]==list_y[-3]: index.append('f')

          else:
            if df['y'][i] == list_zy[-1]: index.append('g')
            elif df['y'][i] == list_zy[-2]: index.append('h')
            elif df['y'][i] == list_zy[-3]: index.append('i')
            else: 
              if df['x'][i]==list_zx[-1]: index.append('j')
              elif df['x'][i]==list_zx[-2]: index.append('k')
              elif df['x'][i]==list_zx[-3]: index.append('l')
    df['index'] = index
    sorted_df =df.sort_values('index').reset_index(drop=True)
    with open(path+'result_extract.txt','a+') as f:
      f.truncate(0)
      f.seek(0)
      f.write('/POST1'+'\n')
      for i in range(len(df['x'])):
        temp_index = df['index'][i]
        temp_node = df['node'][i]
        if temp_index=='a' or temp_index== 'b' or temp_index== 'c':
          f.write('*get,'+str(temp_index)+',node,'+str(temp_node)+',s,z'+'\n')
        elif temp_index == 'd'or temp_index== 'e'or temp_index== 'f'or temp_index== 'g'or temp_index== 'h'or temp_index== 'i':
          f.write('*get,'+str(temp_index)+',node,'+str(temp_node)+',s,y'+'\n')   
        elif temp_index == 'j'or temp_index== 'k'or temp_index== 'l':
          f.write('*get,'+str(temp_index)+'x,node,'+str(temp_node)+',s,x'+'\n')    
          f.write('*get,'+str(temp_index)+'y,node,'+str(temp_node)+',s,y'+'\n')
          f.write('*get,'+str(temp_index)+'xy,node,'+str(temp_node)+',s,xy'+'\n')  
      f.write('''PARSAV,SCALAR,'result','txt','''''+'\n')
      f.write('''/CWD,'''+"'"+directory+str(count+1)+"'"+ '\n')
      f.write('''/filnam, '''+ str(count+1)+'\n')
      f.write('''/title, '''+ str(count+1)+'\n')
      f.write('resume,'+str(count+1)+',db'+'\n')
      f.write('''/INPUT,'result_extract','txt','''+"'"+directory+str(count+1)+'''\\',, 0'''+'\n')
