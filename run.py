import yaml
from datetime import datetime

from po_generator import Po_generator
from po_data_gen import gen_po_data

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

if __name__ == '__main__':
    po_gen_config = config['po_generator']
    data_gen_config = config['data_generator']
    num_pos = config['run']['num_pos']
    print('####################')
    print(f'Generating {num_pos} POs...')
    print('####################')

    for _ in range(config['run']['num_pos']):
        with Po_generator(config = po_gen_config) as pg:
            start = datetime.now()
            pg.login()
            pg.create_po(gen_po_data(
                num_items=data_gen_config['num_items'],
                max_qty=data_gen_config['max_qty'],
                split=data_gen_config['split']
            ))
            end = datetime.now()
            pg.logging(end - start)
    log_file = po_gen_config['log']
    print(f'\n\n{num_pos} POs Created. Find the PO numbers in {log_file}.')