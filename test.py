from references_parser.parsers import SsauParser


test_bibtex = """
@article{brando2003satellite,
  title={Satellite hyperspectral remote sensing for estimating estuarine and coastal water quality},
  author={Brando, Vittorio Ernesto and Dekker, Arnold G},
  journal={IEEE transactions on geoscience and remote sensing},
  volume={41},
  number={6},
  pages={1378--1387},
  year={2003},
  publisher={IEEE}
}

@inproceedings{loizzo2018prisma,
  title={PRISMA: The Italian hyperspectral mission},
  author={Loizzo, Rosa and Guarini, Rocchina and Longo, Francesco and Scopa, Tiziana and Formaro, Roberto and Facchinetti, Claudia and Varacalli, Giancarlo},
  booktitle={IGARSS 2018-2018 IEEE International Geoscience and Remote Sensing Symposium},
  pages={175--178},
  year={2018},
  organization={IEEE}
}

@article{lu2020recent,
  title={Recent advances of hyperspectral imaging technology and applications in agriculture},
  author={Lu, Bing and Dao, Phuong D and Liu, Jiangui and He, Yuhong and Shang, Jiali},
  journal={Remote Sensing},
  volume={12},
  number={16},
  pages={2659},
  year={2020},
  publisher={Multidisciplinary Digital Publishing Institute}
}

@inproceedings{vibhute2015hyperspectral,
  title={Hyperspectral imaging data atmospheric correction challenges and solutions using QUAC and FLAASH algorithms},
  author={Vibhute, Amol D and Kale, KV and Dhumal, Rajesh K and Mehrotra, SC},
  booktitle={2015 International Conference on Man and Machine Interfacing (MAMI)},
  pages={1--6},
  year={2015},
  organization={IEEE}
}

@article{pennisi2016skin,
  title={Skin lesion image segmentation using Delaunay Triangulation for melanoma detection},
  author={Pennisi, Andrea and Bloisi, Domenico D and Nardi, Daniele and Giampetruzzi, Anna Rita and Mondino, Chiara and Facchiano, Antonio},
  journal={Computerized Medical Imaging and Graphics},
  volume={52},
  pages={89--103},
  year={2016},
  publisher={Elsevier}
}

@article{sammouda2014agriculture,
  title={Agriculture satellite image segmentation using a modified artificial Hopfield neural network},
  author={Sammouda, Rachid and Adgaba, Nuru and Touir, Ameur and Al-Ghamdi, Ahmed},
  journal={Computers in Human Behavior},
  volume={30},
  pages={436--441},
  year={2014},
  publisher={Elsevier}
}

@inproceedings{sagar2021semantic,
  title={Semantic segmentation with multi scale spatial attention for self driving cars},
  author={Sagar, Abhinav and Soundrapandiyan, RajKumar},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={2650--2656},
  year={2021}
}

@article{asrar1984estimating,
  title={Estimating absorbed photosynthetic radiation and leaf area index from spectral reflectance in wheat 1},
  author={Asrar, GQ and Fuchs, M and Kanemasu, ET and Hatfield, JL},
  journal={Agronomy journal},
  volume={76},
  number={2},
  pages={300--306},
  year={1984},
  publisher={Wiley Online Library}
}

@article{bohning1992multinomial,
  title={Multinomial logistic regression algorithm},
  author={B{\"o}hning, Dankmar},
  journal={Annals of the institute of Statistical Mathematics},
  volume={44},
  number={1},
  pages={197--200},
  year={1992},
  publisher={Springer}
}

"""


if __name__ == '__main__':
    parser = SsauParser()
    result = parser(test_bibtex)
    for entry in result:
        print(entry, end="\n\n")
