# -*- coding: utf-8 -*-
'''
@Time   :  2020-Mar-15 21:07
@Author :  Shang Yehua
@Email  :  niceshang@outlook.com
@Desc   :  
        日志设置
'''

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))+"/../")
log_path = os.path.join(BASE_DIR, 'logs')
log_size = 1024*1024*10   # 文件大小，10M
backup_count = 10

LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname} {asctime} {process:d} {thread:d} {module}-{filename}-{funcName}:{lineno}] {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'default': {
            'format': '[{levelname} {asctime} {module}-{filename}-{funcName}:{lineno}] {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console_debug': {
            'level': logging.INFO,
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_debug': {
            'level': logging.DEBUG,
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/verbose.log'.format(log_path),
            'maxBytes': log_size,
            'backupCount': backup_count,
            'formatter': 'verbose'
        },
        'file_info': {
            'level': logging.INFO,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/all.log'.format(log_path),
            'maxBytes': log_size,
            'backupCount': backup_count,
            'formatter': 'default'
        },
        'file_error': {
            'level': logging.ERROR,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{0}/error.log'.format(log_path),
            'maxBytes': log_size,
            'backupCount': backup_count,
            'formatter': 'default'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_debug'],
            'propagate': True
        },
        'datalab.assemblyline': {
            'handlers': ['console', 'file_info', 'file_error', 'file_debug'],
            'propagate': True
        }
    }
}
