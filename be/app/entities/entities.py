class Project:
    def __init__(self):
        self.projectName = ''
        self.projectType = ''
        self.entityTypes = ''


class ReturnInfo:
    def __init__(self):
        self.errCode = 0
        self.errMsg = ''
        self.info = []


class QueryAnno:
    def __init__(self):
        self.annoDetails = []
        self.fileContent = ''
        # self.isAnno = False


class AnnoContents:
    def __init__(self):
        self.fileName = ''
        self.annoDetails = None
        self.isAnno = False


class FileInfo:
    def __init__(self):
        self.fileName = ''
        self.isAnno = False


class OutputAnno:
    def __init__(self):
        self.all_anno = []

    def add_anno(self, anno_cont: AnnoContents):

        isTrue = self.is_anno(anno_cont.fileName)
        if not isTrue:
            self.all_anno.append(anno_cont)
        else:
            for ind, anno_info in enumerate(self.all_anno):
                if isinstance(anno_info, dict) and anno_info.get("fileName") == anno_cont.fileName:
                    self.all_anno.pop(ind)
                    self.all_anno.append(anno_cont)

    def is_anno(self, file_name):
        anno_file_names = list(k.get('fileName') for k in self.all_anno if isinstance(k, dict))
        if file_name in anno_file_names:
            return True
        return False

    def get_anno(self, file_name):
        isTrue = self.is_anno(file_name)
        if isTrue:
            for ind, anno_info in enumerate(self.all_anno):
                if isinstance(anno_info, dict) and anno_info.get("fileName") == file_name:
                    return anno_info.get("annoDetails")
        return None






