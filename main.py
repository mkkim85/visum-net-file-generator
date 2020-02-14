df_lri_columns = ['$LINEROUTEITEM:LINENAME', 'LINEROUTENAME', 'DIRECTIONCODE', 'INDEX', 'ISROUTEPOINT', 'NODENO', 'STOPPOINTNO', 'POSTLENGTH', 'ADDVAL']
df_line_route_items = pd.DataFrame(columns=df_lri_columns)
df_line_route_items.to_csv('output/line_route_items.csv', index=False, encoding='utf-8-sig')

# df_tpi_columns = ['$TIMEPROFILEITEM:LINENAME', 'LINEROUTENAME', 'DIRECTIONCODE', 'TIMEPROFILENAME', 'INDEX', 'LRITEMINDEX', 'ALIGHT', 'BOARD', 'ARR', 'DEP', 'NUMFAREPOINTS', 'NUMFAREPOINTSBOARD', 'NUMFAREPOINTSTHROUGH', 'NUMFAREPOINTSALIGHT', 'ADDVAL', '행번호', '정류장순서']
df_tpi_columns = ['$TIMEPROFILEITEM:LINENAME', 'LINEROUTENAME', 'DIRECTIONCODE', 'TIMEPROFILENAME', 'INDEX', 'LRITEMINDEX', 'ALIGHT', 'BOARD', 'ARR', 'DEP', 'NUMFAREPOINTS', 'NUMFAREPOINTSBOARD', 'NUMFAREPOINTSTHROUGH', 'NUMFAREPOINTSALIGHT', 'ADDVAL']
df_time_profile_items = pd.DataFrame(columns=df_tpi_columns)
df_time_profile_items.to_csv('output/time_profile_items.csv', index=False, encoding='utf-8-sig')

df_vji_columns = ['$VEHJOURNEY:NO', 'NAME', 'DEP', 'LINENAME', 'LINEROUTENAME', 'DIRECTIONCODE', 'TIMEPROFILENAME', 'FROMTPROFITEMINDEX', 'TOTPROFITEMINDEX', 'OPERATORNO', 'ADDVAL1', 'ADDVAL2', 'ADDVAL3', 'SERVTRIPPATNO']
df_vehicle_journey_items = pd.DataFrame(columns=df_vji_columns)
df_vehicle_journey_items.to_csv('output/vehicle_journeys.csv', index=False, encoding='utf-8-sig')

df_vjs_columns = ['$VEHJOURNEYSECTION:VEHJOURNEYNO', 'NO', 'FROMTPROFITEMINDEX', 'TOTPROFITEMINDEX', 'VALIDDAYSNO', 'VEHCOMBNO', 'VEHCOMBSET', 'ISOPTIONALREINFORCEMENT', 'PREPREPTIME', 'USESPECPREPREPTIME', 'POSTPREPTIME', 'USESPECPOSTPREPTIME', 'OPERATINGPERIODNO']
df_vehicle_journey_sections = pd.DataFrame(columns=df_vjs_columns)
df_vehicle_journey_sections.to_csv('output/vehicle_journey_sections.csv', index=False, encoding='utf-8-sig')

MAX_INDEX = {}

DIRECTIONCODE = '>'
POSTLENGTH = '0km'
ADDVAL = 0

ARR = '00:00:00'
DEP = '00:00:00'

INDEX = 1; SINDEX = 1; N_CNT = 0; S_CNT = 0; JINDEX = 1
F_NODE = np.nan; T_NODE = np.nan; prev_route_id = np.nan; prev_stop = np.nan; prev_link = np.nan; prev_link_no = np.nan; prev_route_name = np.nan

df_link = df_link_id
# df_link = df_link_id[df_link_id['ROUTE_NAME'] == '535']
# df_link = df_link_id[(df_link_id['ROUTE_NAME'] == '61A') | (df_link_id['ROUTE_NAME'] == '38B') | (df_link_id['ROUTE_NAME'] == '7')]
for _, l in tqdm_notebook(df_link.iterrows(), total=df_link.shape[0]):
    route_id = l['ROUTE_ID']; route_name = l['ROUTE_NAME']; link_id = l['LINK_ID']; link_idx = l['INDEX']

    if prev_route_id != route_id:
        for i, item in df_line_route_items.iloc[::-1].iterrows():
            if item['ISROUTEPOINT'] == 1:
                break;
            df_line_route_items = df_line_route_items.drop(i, 0)
        
        for i, item in df_time_profile_items.iloc[::-1].iterrows():
            if item['ALIGHT'] == 0 and item['BOARD'] == 0:
                df_time_profile_items = df_time_profile_items.drop(i, 0)
            if item['ALIGHT'] == 1 and item['BOARD'] == 1:
                df_time_profile_items.loc[i, 'BOARD'] = 0
                break;
        
        if SINDEX > 1:
            df_route = df_route_info[df_route_info['ISC노선ID'] == prev_route_id]
            if len(df_route) != 0:
                for i in range(1, int(df_route['인가운행횟수']) + 1):
                    dep_time = timedelta_to_hhmmss(pd.to_timedelta(df_route['기점첫차시간'].item()) + (pd.to_timedelta(df_route['배차간격'].item()) * i))
                    df_vehicle_journey_items = df_vehicle_journey_items.append(pd.Series([JINDEX, '', dep_time, prev_route_id, prev_route_name, DIRECTIONCODE, 1, 1, MAX_INDEX[prev_route_id], '', 0, 0, 0, 0], index=df_vji_columns), ignore_index=True)
                    df_vehicle_journey_sections = df_vehicle_journey_sections.append(pd.Series([JINDEX, 1, 1, MAX_INDEX[prev_route_id], 1, '', '', 0, '0s', 0, '0s', 0, ''], index=df_vjs_columns), ignore_index=True)
                    JINDEX = JINDEX + 1
                
        df_line_route_items.to_csv('output/line_route_items.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
        df_line_route_items = pd.DataFrame(columns=df_lri_columns) 
        
        df_time_profile_items.to_csv('output/time_profile_items.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
        df_time_profile_items = pd.DataFrame(columns=df_tpi_columns)
        
        df_vehicle_journey_items.to_csv('output/vehicle_journeys.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
        df_vehicle_journey_items = pd.DataFrame(columns=df_vji_columns)
        
        df_vehicle_journey_sections.to_csv('output/vehicle_journey_sections.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
        df_vehicle_journey_sections = pd.DataFrame(columns=df_vjs_columns)
        
        INDEX = 1; SINDEX = 1; N_CNT = 0; S_CNT = 0;
        F_NODE = np.nan; T_NODE = np.nan; prev_stop = np.nan; prev_link = np.nan; prev_link_no = np.nan;
        df_time = df_time_item[df_time_item['ISC노선ID'] == route_id]
        df_time_len = len(df_time)
        ARR = '00:00:00'
        DEP = '00:00:00'
    prev_route_id = route_id
    prev_route_name = route_name
    
    if prev_link == link_id:
        continue
    prev_link = link_id
    
    n = len(set(df_visum_link[(df_visum_link['LINK_ID'] == link_id)]['LINK_NO']))    
    for i in range(n):
        if np.isnan(T_NODE):
            df_vlink = df_visum_link[df_visum_link['LINK_ID'] == link_id]
        else:
            df_vlink = df_visum_link[(df_visum_link['LINK_ID'] == link_id) & (df_visum_link['F_NODE'] == T_NODE) & (df_visum_link['T_NODE'] != F_NODE) ]
        
        for _, vl in df_vlink.iterrows():
            link_no = vl['LINK_NO']
            if prev_link_no == link_no:
                continue
            prev_link_no = link_no
            
            if np.isnan(T_NODE):
                df_vstop = (df_visum_stop[df_visum_stop['LINK_NO'] == link_no]).sort_values(by=['INDEX', 'F_NODE'])
            else:
                df_vstop = (df_visum_stop[(df_visum_stop['LINK_NO'] == link_no) & (df_visum_stop['F_NODE'] == T_NODE)]).sort_values(by=['INDEX', 'F_NODE'])
            
            for _, vs in df_vstop.iterrows():
                if prev_stop == vs['STOP_NO']:
                    continue
                prev_stop = vs['STOP_NO']
                
                if INDEX == 1:
                    F_NODE = vs['F_NODE']
                    T_NODE = df_visum_link[(df_visum_link['LINK_ID'] == link_id) & (df_visum_link['F_NODE'] == F_NODE) & (df_visum_link['LINK_NO'] == link_no)].T_NODE.item()                
                stop_info = df_time[(df_time['VISUM정류소NO'] == str(vs['STOP_NO'])) & (df_time['정류소순번'] == str(SINDEX))].head(1)
#                 if len(stop_info) == 0:
#                     stop_info = df_time[df_time['정류소순번'] == str(SINDEX)].head(1)
#                 stop_info = df_time[df_time['VISUM정류소NO'] == str(vs['STOP_NO'])].head(1)
#                 stop_info = df_time[df_time['정류소순번'] == str(SINDEX)].head(1)

                if df_time_len == 0:
                    if SINDEX == 1:
#                         df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 0, 1, '00:00:00', '00:00:00', 0, 0, 0, 0, 0, INDEX, SINDEX], index=df_tpi_columns), ignore_index=True)
                        df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 0, 1, '00:00:00', '00:00:00', 0, 0, 0, 0, 0], index=df_tpi_columns), ignore_index=True)
                    else:
#                         df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 1, 1, '00:00:00', '00:00:00', 0, 0, 0, 0, 0, INDEX, SINDEX], index=df_tpi_columns), ignore_index=True)
                        df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 1, 1, '00:00:00', '00:00:00', 0, 0, 0, 0, 0], index=df_tpi_columns), ignore_index=True)
                    MAX_INDEX[route_id] = SINDEX
                    df_line_route_items = df_line_route_items.append(pd.Series([route_id, route_name, DIRECTIONCODE, INDEX, 1, '', vs['STOP_NO'], POSTLENGTH, ADDVAL], index=df_lri_columns), ignore_index=True)
                    INDEX = INDEX + 1 
                    SINDEX = SINDEX + 1
                    S_CNT = S_CNT + 1
                elif len(stop_info) != 0:
                        if SINDEX == 1:
    #                         df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 0, 1, stop_info['ARR'].item(), stop_info['DEP'].item(), 0, 0, 0, 0, 0, stop_info.index[0], stop_info['정류소순번'].item()], index=df_tpi_columns), ignore_index=True)
                            df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 0, 1, stop_info['ARR'].item(), stop_info['DEP'].item(), 0, 0, 0, 0, 0], index=df_tpi_columns), ignore_index=True)
                        else:
    #                         df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 1, 1, stop_info['ARR'].item(), stop_info['DEP'].item(), 0, 0, 0, 0, 0, stop_info.index[0], stop_info['정류소순번'].item()], index=df_tpi_columns), ignore_index=True)
                            df_time_profile_items = df_time_profile_items.append(pd.Series([route_id, route_name, '>', 1, SINDEX, INDEX, 1, 1, stop_info['ARR'].item(), stop_info['DEP'].item(), 0, 0, 0, 0, 0], index=df_tpi_columns), ignore_index=True)
                        MAX_INDEX[route_id] = SINDEX
                        ARR = stop_info['DEP'].item()
                        DEP = ARR
                        df_time = df_time.drop(stop_info.index)
                        df_line_route_items = df_line_route_items.append(pd.Series([route_id, route_name, DIRECTIONCODE, INDEX, 1, '', vs['STOP_NO'], POSTLENGTH, ADDVAL], index=df_lri_columns), ignore_index=True)
                        INDEX = INDEX + 1 
                        SINDEX = SINDEX + 1
                        S_CNT = S_CNT + 1
            
            if S_CNT > 0 and N_CNT == 0:
                if F_NODE != T_NODE:
                    df_line_route_items = df_line_route_items.append(pd.Series([route_id, route_name, DIRECTIONCODE, INDEX, 0, T_NODE, '', POSTLENGTH, ADDVAL], index=df_lri_columns), ignore_index=True)
                    INDEX = INDEX + 1
                    N_CNT = N_CNT + 1
                    prev_stop = np.nan
                break
            else:
                F_NODE = T_NODE
                T_NODE = vl['T_NODE']
                if F_NODE != T_NODE and INDEX > 1:
                    df_line_route_items = df_line_route_items.append(pd.Series([route_id, route_name, DIRECTIONCODE, INDEX, 0, T_NODE, '', POSTLENGTH, ADDVAL], index=df_lri_columns), ignore_index=True)
                    INDEX = INDEX + 1
                    N_CNT = N_CNT + 1
                    prev_stop = np.nan
                
for i, item in df_line_route_items.iloc[::-1].iterrows():
    if item['ISROUTEPOINT'] == 1:
        break;
    df_line_route_items = df_line_route_items.drop(i, 0)

for i, item in df_time_profile_items.iloc[::-1].iterrows():
    if item['ALIGHT'] == 0 and item['BOARD'] == 0:
        df_time_profile_items = df_time_profile_items.drop(i, 0)
    if item['ALIGHT'] == 1 and item['BOARD'] == 1:
        df_time_profile_items.loc[i, 'BOARD'] = 0
        break;
        
if SINDEX > 1:
    df_route = df_route_info[df_route_info['ISC노선ID'] == prev_route_id]
    if len(df_route) != 0:
        for i in range(1, int(df_route['인가운행횟수']) + 1):
            dep_time = timedelta_to_hhmmss(pd.to_timedelta(df_route['기점첫차시간'].item()) + (pd.to_timedelta(df_route['배차간격'].item()) * i))
            df_vehicle_journey_items = df_vehicle_journey_items.append(pd.Series([JINDEX, '', dep_time, prev_route_id, prev_route_name, DIRECTIONCODE, 1, 1, MAX_INDEX[prev_route_id], '', 0, 0, 0, 0], index=df_vji_columns), ignore_index=True)
            df_vehicle_journey_sections = df_vehicle_journey_sections.append(pd.Series([JINDEX, 1, 1, MAX_INDEX[prev_route_id], 1, '', '', 0, '0s', 0, '0s', 0, ''], index=df_vjs_columns), ignore_index=True)
            JINDEX = JINDEX + 1
    
df_line_route_items.to_csv('output/line_route_items.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
df_time_profile_items.to_csv('output/time_profile_items.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
df_vehicle_journey_items.to_csv('output/vehicle_journeys.csv', mode='a', index=False, encoding='utf-8-sig', header=False)
df_vehicle_journey_sections.to_csv('output/vehicle_journey_sections.csv', mode='a', index=False, encoding='utf-8-sig', header=False)