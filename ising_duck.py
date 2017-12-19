# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import cv2
from tqdm import tqdm

# みんな大好きイジングモデル
class ising():
    # しょきか
    def __init__(self, tate = 5, yoko = 5, h = 0, T = 2.0, initialize = "random"):
        # モデルサイズ
        self.tate = tate
        self.yoko = yoko

        # ポテンシャルエネルギー
        self.h = h

        # 外部温度かな わかりません
        self.T = T

        # 各ノードの状態
        self.nodes = []
        if initialize == "random":
            self.nodes = np.random.choice([-1, 1], (self.tate, self.yoko))
        elif initialize == "one":
            self.nodes = np.ones((self.tate, self.yoko))
        elif initialize == "minus":
            self.nodes = -1 * np.ones((self.tate, self.yoko))
        else:
            self.nodes = cv2.imread(initialize, cv2.IMREAD_GRAYSCALE)
            self.nodes = (self.nodes / 255) * 2 - 1
            self.nodes = self.nodes.astype(np.int32)
            self.tate = len(self.nodes)
            self.yoko = len(self.nodes[0])

        # ノード間の関係
        self.edges_yoko = np.zeros((self.tate, self.yoko-1))
        self.edges_tate = np.zeros((self.tate-1, self.yoko))
        for i in range(self.tate):
            for j in range(self.yoko):
                if i != self.tate - 1:
                    self.edges_tate[i][j] = self.nodes[i][j] * self.nodes[i + 1][j]
                if j != self.yoko - 1:
                    self.edges_yoko[i][j] = self.nodes[i][j] * self.nodes[i][j+1]
        number = sum(sum(self.edges_yoko)) + sum(sum(self.edges_tate))

        cv2.imwrite("./results/yoko.png", (self.edges_yoko - 1) * -127)
        cv2.imwrite("./results/tate.png", (self.edges_tate - 1) * -127)

    # 指定した頂点が関与するエネルギーを計算
    def keisan_mawari(self, image, i, j):
        energy = 0.

        # 初項
        if j != 0:
            energy -= self.edges_yoko[i][j-1] * image[i][j-1] * image[i][j]
        if j != self.yoko - 1:
            energy -= self.edges_yoko[i][j] * image[i][j] * image[i][j+1]
        if i != 0:
            energy -= self.edges_tate[i-1][j] * image[i-1][j] * image[i][j]
        if i != self.tate - 1:
            energy -= self.edges_tate[i][j] * image[i][j] * image[i+1][j]

        # 第二項
        energy -= self.h * image[i][j]

        return energy

    # 全体のエネルギーを計算
    def keisan_energy(self, image):
        energy = 0.

        for i in range(self.tate):
            for j in range(self.yoko):
                # 初項
                if j != 0:
                    energy -= self.edges_yoko[i][j-1] * image[i][j-1] * image[i][j]
                if j != self.yoko - 1:
                    energy -= self.edges_yoko[i][j] * image[i][j] * image[i][j+1]
                if i != 0:
                    energy -= self.edges_tate[i-1][j] * image[i-1][j] * image[i][j]
                if i != self.tate - 1:
                    energy -= self.edges_tate[i][j] * image[i][j] * image[i+1][j]

                # 第二項
                energy -= self.h * image[i][j]

        return energy

    # 反転する確率の計算 シグモイドっぽい形
    def kakuritsu(self, energy, tate, yoko):
        return 1. / (1. + np.exp(-2. * (energy + self.h) / self.T))

    # 指定した初期値からスピンの動きをシミュレーション
    def main(self, initialize = "random"):
        # 初期値設定
        if initialize == "random":
            gazo = np.random.choice([-1, 1], (self.tate, self.yoko))
        elif initialize == "one":
            gazo = np.ones((self.tate, self.yoko))
        else:
            gazo = -1 * np.ones((self.tate, self.yoko))
        cv2.imwrite("./results/origin.png", (gazo - 1) * -127)

        """ きれいに走査をn回
        for l in tqdm(range(100)):
            for i in range(len(gazo)):
                for j in range(len(gazo[0])):
                    tate = i
                    yoko = j

                    ene = self.keisan_mawari(gazo, tate, yoko)

                    if np.random.rand() < self.kakuritsu(ene, tate, yoko):
                        gazo[tate][yoko] *= -1
            cv2.imwrite("./results/" + str(l) + ".png", (gazo + 1) * 127)
        #"""

        """ エネルギー変化が起こらなかったら終了
        continu = True
        prev_energy = 1010101010101
        count = 0
        while(continu == True):
            for i in range(len(gazo)):
                for j in range(len(gazo[0])):
                    tate = i
                    yoko = j

                    ene = self.keisan_mawari(gazo, tate, yoko)

                    if np.random.rand() < self.kakuritsu(ene, tate, yoko):
                        gazo[tate][yoko] *= -1
            cv2.imwrite("./results/" + str(count) + ".png", (gazo - 1) * -127)
            energy = self.keisan_energy(gazo)
            if energy == prev_energy:
                continu = False
            prev_energy = energy
            print(str(count) + "," + str(energy))
            count += 1
        #"""

        #""" ランダムにn回動かす
        for l in tqdm(range(1000)):
            for i in range(self.tate * self.yoko):
                tate = np.random.randint(self.tate)
                yoko = np.random.randint(self.yoko)

                ene = self.keisan_mawari(gazo, tate, yoko)

                if np.random.rand() < self.kakuritsu(ene, tate, yoko):
                    gazo[tate][yoko] *= -1
            cv2.imwrite("./results/" + str(l) + ".png", (gazo - 1) * -127)
            #energy = self.keisan_energy(gazo)
            #print(str(l) + "," + str(energy))
        #"""

        cv2.imwrite("./results/result.png", (gazo - 1) * -127)

if __name__ == "__main__":
    #aidd = ising(tate = 3, yoko = 3, h = 0.0, T = 0.2, initialize = "duck_100x56.png")
    aidd = ising(h = -0.001, T = 0.05, initialize = "duck_aidu.png")
    print("origin : " + str(aidd.keisan_energy(aidd.nodes)))
    aidd.main("random")
