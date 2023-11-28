
import GLOBALS as global_s
import pandas as pd
import GLOBALS

class XlsxDatas :
    def __init__(self) -> None:
        self._samplesFilePath = global_s.BASE_DIR + "/samples/{}.xlsx".format(GLOBALS.DB_FILE_NAME)
        self.column_names = []
        self.datas = None
        pass
    pass

    def readDatas(self) :
        datafr = pd.read_excel(self._samplesFilePath, header=0)
        self.column_names = list(datafr)
        print(self.column_names)
        self.datas = datafr
        print(self.datas.head(5))
        pass

