import random

vendor_nums = [
    '00251236',
    '00305098',
    '00305099',
    '00973306',
    '00065965',
    '00840366',
    '00111520',
    '00004487',
    '00007667',
    '00012112'
]

CODE_DATE = []
CATCH_WGT = []
NORMAL = []
with open('product_numbers/code_date_prod_exetraining.txt') as f:
    CODE_DATE = f.read().splitlines()
with open('product_numbers/catch_wgt_prod_exetraining.txt') as f:
    CATCH_WGT = f.read().splitlines()
with open('product_numbers/normal_prod_exetraining.txt') as f:
    NORMAL = f.read().splitlines()

def gen_po_data(num_items = 25, max_qty = 500, split = [1, 0, 0]):
    po_data = {}
    po_data['vendor'] = random.choice(vendor_nums)
    products = {}

    cw_num = round(split[0] * num_items)
    cd_num = round(split[1] * num_items)
    normal_num = num_items - cw_num - cd_num
    p_ids = []
    if cw_num > 0:
        p_ids += random.sample(CATCH_WGT, cw_num)
    if cd_num > 0:
        p_ids += random.sample(CODE_DATE, cd_num)
    if normal_num > 0:
        p_ids += random.sample(NORMAL, normal_num)
    for p_id in p_ids:
        products[p_id] = str(random.randint(1, max_qty))
    po_data['products'] = products
    return po_data