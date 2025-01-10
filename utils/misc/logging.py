import os
import logging
from datetime import datetime

os.makedirs(name='data/logs', exist_ok=True)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG,
                    filename=f"data/logs/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log",
                    filemode='w'
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )
