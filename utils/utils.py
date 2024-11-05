"""Utilities Functions for PNR Scrapping"""


def get_model(app_name, model_name):
    """Returns Model Instance"""
    from django.apps import apps

    return apps.get_model(app_label=app_name, model_name=model_name)
