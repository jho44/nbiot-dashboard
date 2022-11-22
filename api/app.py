import json
import datetime

from flask import Flask
from flask_cors import CORS, cross_origin
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def home():
  f = open('boop.json')
  raw_blocks = json.load(f)
  f.close()

  return get_resource_assignments(raw_blocks)
  return 'Hello, Flask!'

airtime = {
  0: 1,
  1: 2,
  2: 3,
  3: 4,
  4: 5,
  5: 6,
  6: 8,
  7: 10
}

@app.route('/blocks')
@cross_origin()
def blocks():
    dl_block1 = {'log_msg_len': 40, 'type_id': 'LTE_MAC_DL_Transport_Block', 'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 8, 440769), 'Version': 1, 'Num SubPkt': 1, 'Subpackets': [{'SubPacket ID': 'DL Transport Block', 'Version': 2, 'SubPacket Size': 24, 'Num Samples': 1, 'Samples': [
      {
        'Resource Assignment': 2, 'Sub-FN': 3, 'SFN': 238, 'RNTI Type': 'C-RNTI', 'HARQ ID': 0, 'Area ID': 0, 'PMCH ID': 0, 'DL TBS (bytes)': 85, 'RLC PDUs': 2, 'Padding (bytes)': 1, 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 35, 'LC ID': '3', 'Len': 2}, {'Header Field': 35, 'LC ID': '3', 'Len': 77}, {'Header Field': 31, 'LC ID': 'Padding', 'Len': -1}]}]}]}
    dl_block2 = {
      'log_msg_len': 40,
      'type_id': 'LTE_MAC_DL_Transport_Block',
      'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 9, 191456),
      'Version': 1,
      'Num SubPkt': 1,
      'Subpackets': [
        {
          'SubPacket ID': 'DL Transport Block',
          'Version': 2,
          'SubPacket Size': 24,
          'Num Samples': 1,
          'Samples': [
            {
              'Resource Assignment': 1,
              'Sub-FN': 6,
              'SFN': 312,
              'RNTI Type': 'RA-RNTI',
              'HARQ ID': 0,
              'Area ID': 0,
              'PMCH ID': 0,
              'DL TBS (bytes)': 7,
              'RLC PDUs': 0,
              'Padding (bytes)': 0,
              'HDR LEN': 7
            }]}]}
    ul_block1 = {'log_msg_len': 76, 'type_id': 'LTE_MAC_UL_Transport_Block', 'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 8, 745830), 'Version': 1, 'Num SubPkt': 1, 'Subpackets': [{'SubPacket ID': 'UL Transport Block', 'Version': 1, 'SubPacket Size': 60, 'Num Samples': 3, 'Samples': [
      {'Resource Assignment': 1, 'HARQ ID': 0, 'RNTI Type': 'RA-RNTI', 'Sub-FN': 9, 'SFN': 233, 'Grant (bytes)': 11, 'RLC PDUs': 1, 'Padding (bytes)': 0, 'BSR event': 'High Data Arrival', 'BSR trig': 'S-BSR', 'HDR LEN': 6},
      {'Resource Assignment': 2, 'HARQ ID': 0, 'RNTI Type': 'C-RNTI', 'Sub-FN': 1, 'SFN': 236, 'Grant (bytes)': 77, 'RLC PDUs': 1, 'Padding (bytes)': 0, 'BSR event': 'Periodic', 'BSR trig': 'S-BSR', 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 63, 'LC ID': 'Padding', 'Len': -1}, {'Header Field': 63, 'LC ID': 'Padding', 'Len': -1}, {'Header Field': 61, 'LC ID': 'S-BSR', 'Len': 1, 'S/T-BSR Field': 0, 'BSR LCG 0': 0, 'BSR LCG 0 (bytes)': 0}, {'Header Field': 3, 'LC ID': '3', 'Len': 0}]},
      {'Resource Assignment': 3, 'HARQ ID': 0, 'RNTI Type': 'C-RNTI', 'Sub-FN': 7, 'SFN': 241, 'Grant (bytes)': 77, 'RLC PDUs': 1, 'Padding (bytes)': 70, 'BSR event': 'High Data Arrival', 'BSR trig': 'S-BSR', 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 61, 'LC ID': 'S-BSR', 'Len': 1, 'S/T-BSR Field': 0, 'BSR LCG 0': 0, 'BSR LCG 0 (bytes)': 0}, {'Header Field': 35, 'LC ID': '3', 'Len': 2}, {'Header Field': 31, 'LC ID': 'Padding', 'Len': -1}]}]}]}
    ul_block2 = {
      'log_msg_len': 76,
      'type_id': 'LTE_MAC_UL_Transport_Block',
      'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 9, 765828),
      'Version': 1,
      'Num SubPkt': 1,
      'Subpackets': [
        {
          'SubPacket ID': 'UL Transport Block',
          'Version': 1,
          'SubPacket Size': 60,
          'Num Samples': 3,
          'Samples': [
            {
              'Resource Assignment': 1,
              'HARQ ID': 0,
              'RNTI Type': 'RA-RNTI',
              'Sub-FN': 9,
              'SFN': 313,
              'Grant (bytes)': 11,
              'RLC PDUs': 1,
              'Padding (bytes)': 0,
              'BSR event': 'High Data Arrival',
              'BSR trig': 'S-BSR',
              'HDR LEN': 6
            }, {
              'Resource Assignment': 2, 'HARQ ID': 0, 'RNTI Type': 'C-RNTI', 'Sub-FN': 1, 'SFN': 316, 'Grant (bytes)': 77, 'RLC PDUs': 1, 'Padding (bytes)': 0, 'BSR event': 'Periodic', 'BSR trig': 'S-BSR', 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 63, 'LC ID': 'Padding', 'Len': -1}, {'Header Field': 63, 'LC ID': 'Padding', 'Len': -1}, {'Header Field': 61, 'LC ID': 'S-BSR', 'Len': 1, 'S/T-BSR Field': 0, 'BSR LCG 0': 0, 'BSR LCG 0 (bytes)': 0}, {'Header Field': 3, 'LC ID': '3', 'Len': 0}]
            }, {
              'Resource Assignment': 1, 'HARQ ID': 0, 'RNTI Type': 'C-RNTI', 'Sub-FN': 7, 'SFN': 321, 'Grant (bytes)': 77, 'RLC PDUs': 1, 'Padding (bytes)': 70, 'BSR event': 'High Data Arrival', 'BSR trig': 'S-BSR', 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 61, 'LC ID': 'S-BSR', 'Len': 1, 'S/T-BSR Field': 0, 'BSR LCG 0': 0, 'BSR LCG 0 (bytes)': 0}, {'Header Field': 35, 'LC ID': '3', 'Len': 2}, {'Header Field': 31, 'LC ID': 'Padding', 'Len': -1}]}]}]}
    dci_block1 = {
      'log_msg_len': 64,
      'type_id': 'LTE_NB1_ML1_GM_DCI_Info',
      'timestamp': 'datetime.datetime(1980, 1, 6, 0, 3, 10, 429347)',
      'Version': 3,
      'Num of Records': 6,
      'Records': [
        {
          'NPDCCH Timing HSFN': 19,
          'NPDCCH Timing SFN': 411,
          'NPDCCH Timing Sub FN': 2,
          'RNTI Type Data': 1,
          'RNTI Type': 'C-RNTI',
          'UL Grant Present': 'True',
          'DL Grant Present': 'False',
          'PDCCH Order Present': 'False',
          'NDI': 1,
          'Reserved': 0,
          'SC Index': 18,
          'Redundancy Version': 0,
          'Resource Assignment': 3,
          'Scheduling Delay': 0,
          'MCS': 9,
          'Repetition Number': 0,
          'DCI Repetition Number': 0,
          'HARQ Resource': 0,
          'Reserved2': 0
        }, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 413, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 0, 'Scheduling Delay': 0, 'MCS': 4, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 416, 'NPDCCH Timing Sub FN': 8, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 1, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 2, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 420, 'NPDCCH Timing Sub FN': 1, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 12, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 422, 'NPDCCH Timing Sub FN': 4, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 2, 'Scheduling Delay': 0, 'MCS': 6, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 425, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 1, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}]}
    dci_block2 = {'log_msg_len': 40, 'type_id': 'LTE_NB1_ML1_GM_DCI_Info', 'timestamp': 'datetime.datetime(1980, 1, 6, 0, 3, 11, 629343)', 'Version': 3, 'Num of Records': 3, 'Records': [{'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 507, 'NPDCCH Timing Sub FN': 2, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 509, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 2, 'Scheduling Delay': 0, 'MCS': 12, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0}, {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 513, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 1, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}]}

    # blocks = [dl_block1, dl_block2, ul_block1, ul_block2, dci_block1, dci_block2]

    # Opening JSON file
    f = open('boop.json')
    raw_blocks = json.load(f)
    f.close()

    blocks = get_resource_assignments(raw_blocks)

    '''
    wanna return list of samples and records, where each has the form:
    {
      'type': 'DL-DCI', # one of ['DL-DCI', 'UL-DCI', 'DL-DATA', 'UL-DATA']
      'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 8, 440769),
      'FN': 2,
      'Sub-FN': 2,
      'airtime': airtime[resource_assignment]
    }
    '''

    content = []

    for block in blocks:
      type_id = 'LTE_MAC_UL_Transport_Block'
      if 'DL TBS (bytes)' in block:
        type_id = 'LTE_MAC_DL_Transport_Block'
      elif 'DCI Repetition Number' in block:
        type_id = 'LTE_NB1_ML1_GM_DCI_Info'
      if type_id == 'LTE_MAC_DL_Transport_Block' or type_id == 'LTE_MAC_UL_Transport_Block':
        content.append({
          'type': 'DL-DATA' if type_id == 'LTE_MAC_DL_Transport_Block' else 'UL-DATA',
          'timestamp': block['timestamp'].strftime('%m/%d/%Y %H:%M:%S.%f'),
          'FN': block['SFN'],
          'Sub-FN': block['Sub-FN'],
          'airtime': airtime[block['Resource Assignment']] # TODO: add Resource Assignment to decoded DL blocks
        })
      else: # LTE_NB1_ML1_GM_DCI_Info
        content.append({
          'type': 'DL-DCI' if block['DL Grant Present'] == 'True' else 'UL-DCI',
          'timestamp': block['timestamp'].strftime('%m/%d/%Y %H:%M:%S.%f'),
          'FN': block['NPDCCH Timing SFN'],
          'Sub-FN': block['NPDCCH Timing Sub FN'],
          # 'airtime': airtime[block['Resource Assignment']] # TODO: add Resource Assignment to decoded DL blocks
          'airtime': 1
        })

    return content

# {'log_msg_len': 40, 'type_id': 'LTE_MAC_DL_Transport_Block', 'timestamp': datetime.datetime(1980, 1, 6, 0, 3, 9, 241346), 'Version': 1, 'Num SubPkt': 1, 'Subpackets': [{'SubPacket ID': 'DL Transport Block', 'Version': 2, 'SubPacket Size': 24, 'Num Samples': 1, 'Samples': [{'Sub-FN': 3, 'SFN': 318, 'RNTI Type': 'C-RNTI', 'HARQ ID': 0, 'Area ID': 0, 'PMCH ID': 0, 'DL TBS (bytes)': 85, 'RLC PDUs': 2, 'Padding (bytes)': 1, 'HDR LEN': 5, 'Mac Hdr + CE': [{'Header Field': 35, 'LC ID': '3', 'Len': 2}, {'Header Field': 35, 'LC ID': '3', 'Len': 77}, {'Header Field': 31, 'LC ID': 'Padding', 'Len': -1}]}]}]}


# {'log_msg_len': 32, 'type_id': 'LTE_NB1_ML1_GM_DCI_Info', 'timestamp': 'datetime.datetime(1980, 1, 6, 0, 3, 9, 829344)', 'Version': 3, 'Num of Records': 2, 'Records': [
#   {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 317, 'NPDCCH Timing Sub FN': 6, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'False', 'DL Grant Present': 'True', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 0, 'Redundancy Version': 0, 'Resource Assignment': 2, 'Scheduling Delay': 0, 'MCS': 12, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 1, 'Reserved2': 0},
#   {'NPDCCH Timing HSFN': 19, 'NPDCCH Timing SFN': 320, 'NPDCCH Timing Sub FN': 8, 'RNTI Type Data': 1, 'RNTI Type': 'C-RNTI', 'UL Grant Present': 'True', 'DL Grant Present': 'False', 'PDCCH Order Present': 'False', 'NDI': 0, 'Reserved': 0, 'SC Index': 18, 'Redundancy Version': 0, 'Resource Assignment': 3, 'Scheduling Delay': 0, 'MCS': 9, 'Repetition Number': 0, 'DCI Repetition Number': 0, 'HARQ Resource': 0, 'Reserved2': 0}]}

def get_resource_assignments(blocks):
  dl_samples_not_found = {}
  ul_samples_not_found = {}
  found_samples = []

  for block in blocks:
    if block['type_id'] == 'LTE_NB1_ML1_GM_DCI_Info':
      for record in block['Records']:
        record['timestamp'] = eval(block['timestamp']) if type(block['timestamp']) == str else block['timestamp']
        frame_num = record['NPDCCH Timing SFN'] * 10 + record['NPDCCH Timing Sub FN']
        if record['RNTI Type'] != 'SI-RNTI':
          end_frame_num = frame_num + 10
          if record['Scheduling Delay'] != 0:
            end_frame_num += 10

          ####### TBD ########
          # if record['UL Grant Present'] == 'True':
          #   print('UL', ul_samples_not_found.keys())
          # else:
          #   print('DL', dl_samples_not_found.keys())

          # print(frame_num, end_frame_num)
          ####### TBD ########

          for i in range(frame_num, end_frame_num):
            if record['UL Grant Present'] == 'True':
              if i in ul_samples_not_found:
                print("UPLINK")
                for ind, lost_sample in enumerate(ul_samples_not_found[i]):
                  if (record['timestamp'] - lost_sample['timestamp']).seconds == 0:
                    lost_sample['Resource Assignment'] = record['Resource Assignment']
                    found_samples.append(lost_sample)
                    found_samples.append(record)
                    if len(ul_samples_not_found[i]) == 1:
                      del ul_samples_not_found[i]
                    else:
                      del ul_samples_not_found[i][ind]
                    break
                break
            else:
              if i in dl_samples_not_found:
                print("DOWNLINK")
                for ind, lost_sample in enumerate(dl_samples_not_found[i]):
                  if (record['timestamp'] - lost_sample['timestamp']).seconds == 0:
                    lost_sample['Resource Assignment'] = record['Resource Assignment']
                    found_samples.append(lost_sample)
                    found_samples.append(record)
                    if len(dl_samples_not_found[i]) == 1:
                      del dl_samples_not_found[i]
                    else:
                      del dl_samples_not_found[i][ind]
                    break
                break
    else: # block['type_id'] == 'LTE_MAC_DL_Transport_Block' or 'LTE_MAC_UL_Transport_Block'
      for packet in block['Subpackets']:
        block['timestamp'] = eval(block['timestamp'])
        for sample in packet['Samples']:
          sample['timestamp'] = block['timestamp']
          SFN = sample['Sub-FN']
          FN = sample['SFN']
          fn = FN * 10 + SFN
          if block['type_id'] == 'LTE_MAC_UL_Transport_Block':
            if fn not in ul_samples_not_found:
              ul_samples_not_found[fn] = [sample]
            else:
              ul_samples_not_found[fn].append(sample)

            # print(ul_samples_not_found.keys())
          else:
            if fn not in dl_samples_not_found:
              dl_samples_not_found[fn] = [sample]
            else:
              dl_samples_not_found[fn].append(sample)

            # print(dl_samples_not_found)

  def get_time_stamp(e):
    return e['timestamp']

  found_samples.sort(key=get_time_stamp)
  return found_samples