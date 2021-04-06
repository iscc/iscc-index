# -*- coding: utf-8 -*-
import os

ISCC_INDEX_ALLOWED_ORIGINS = os.environ.get("ISCC_INDEX_ALLOWED_ORIGINS", "*").split()
