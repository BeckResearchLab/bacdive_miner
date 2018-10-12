#! /usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import yaml


class BacdiveClient(object):
    def __init__(self, credentials):
        self.headers = {'Accept': 'application/json'}
        USERNAME = credentials['login']
        PASSWORD = credentials['password']
        self.credentials = HTTPBasicAuth(USERNAME, PASSWORD)

    def getLinksByGenus(self, genus):
        response = requests.get(
            'http://bacdive.dsmz.de/api/bacdive/taxon/%s/' % (genus ),
            headers=self.headers,
            auth=self.credentials
        )
        if response.status_code == 200:
            results = response.json()
            return results

    def getLinksBySpecies(self, genus, species_epithet):
        response = requests.get(
            'http://bacdive.dsmz.de/api/bacdive/taxon/%s/%s/' % (genus,species_epithet),
            headers=self.headers,
            auth=self.credentials
        )
        if response.status_code == 200:
            results = response.json()
            return results

    def getLinksBySubspecies(self, genus, species_epithet, subspecies_epithet):
        response = requests.get(
            'http://bacdive.dsmz.de/api/bacdive/taxon/%s/%s/%s/' % (genus,species_epithet,subspecies_epithet),
            headers=self.headers,
            auth=self.credentials
        )
        if response.status_code == 200:
            results = response.json()
            return results

    def getLinksBySeqAccNum(self, seq_acc_num):          
        response = requests.get(
            'http://bacdive.dsmz.de/api/bacdive/sequence/%s/' % (seq_acc_num),
            headers=self.headers,
            auth=self.credentials
        )
        if response.status_code == 200:
            results = response.json()
            return results

    def getDataFromURL(self, url):
        response = requests.get(url, headers=self.headers, 
                                auth=self.credentials)
        if response.status_code == 200:
            results = response.json()
            return results

    def run(self):
        genus = self.getLinksByGenus('Methylomonas') 
        print(genus)
        for result in genus['results']:
            url = result['url']
            summary = self.getDataFromURL('https://bacdive.dsmz.de/api/bacdive/bacdive_id/7209/')
            genus = None
            species = None
            subspecies = None
            gt = None
            gr = None
            if 'taxonomy_name' in summary:
                tax = summary['taxonomy_name']
                if 'strains_tax_PNU' in tax:
                    taxlin = tax['strains_tax_PNU'][0]
                    print(taxlin)
                    print(taxlin['species_epithet'])
                    if 'genus' in taxlin:
                        genus = taxlin['genus']
                    if 'species_epithet' in taxlin:
                        species = taxlin['species_epithet']
                    if 'subspecies_epithet' in taxlin:
                        subspecies = taxlin['subspecies_epithet']
            if 'culture_growth_condition' in summary:
                cgc = summary['culture_growth_condition'];
                if 'culture_temp' in cgc:
                    ct = cgc['culture_temp'][0]
                    if 'temp' in ct:
                        gt = ct['temp']
                    if 'temperature_range' in ct:
                        gr = ct['temperature_range']
            print("{}\t{}\t{}\t{}\t{}".format(genus, species, subspecies,
                                                gt, gr))

#        species = self.getLinksBySpecies('Methylomonas','methanica')
#        print(species)
#        subspecies = self.getLinksBySubspecies('Bacillus','subtilis', 'subtilis')
#        print(subspecies)
#        sec_acc_num = self.getLinksBySeqAccNum('ALAS01000001')
#        print(sec_acc_num)

if __name__ == '__main__':
    stream = open('credentials.yaml', 'r')
    credentials = yaml.load(stream)
    BacdiveClient(credentials).run()
