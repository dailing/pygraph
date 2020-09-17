import pandas as pd


class CsvDataset():
    def __init__(self, csvfile, split='train', split_ratio=None, transform=None):
        self.records = pd.read_csv(csvfile)
        self.records = self.records.dropna()
        if split_ratio is not None:
            spp = int(split_ratio*len(self.records))
            if split == 'train':
                self.records = self.records[:spp]
            elif split == 'test':
                self.records = self.records[spp:]
            else:
                raise Exception('FUCK')
        self.transform = transform
    
    def __getitem__(self, index):
        dd = self.records.iloc[index].to_dict()
        return self.transform(dd)
        
    def __len__(self):
        return len(self.records)
