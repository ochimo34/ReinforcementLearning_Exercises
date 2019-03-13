# -*- coding:utf-8 -*-
# Anaconda 5.0.1 環境

import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib import animation

# OpenAI Gym
import gym

# PyTorch
import torch
from torch.utils.data import TensorDataset, DataLoader
from torch  import nn   # ネットワークの構成関連
import torchvision      # 画像処理関連

# 自作モジュール
from Academy import Academy
from CartPoleAcademy import CartPoleAcademy
from CartPoleA2CAcademy import CartPoleA2CAcademy

from Brain import Brain
from CartPoleA2CBrain import CartPoleA2CBrain

from Agent import Agent
from CartPoleAgent import CartPoleAgent


#--------------------------------
# 設定可能な定数
#--------------------------------
RL_ENV = "CartPole-v0"              # 利用する強化学習環境の課題名
NUM_EPISODE = 500                   # エピソード試行回数
NUM_TIME_STEP = 200                 # １エピソードの時間ステップの最大数
NUM_KSTEP = 5                       # 先読みステップ数 k
BRAIN_LEARNING_RATE = 0.0001        # 学習率
BRAIN_GAMMDA = 0.99                 # 利得の割引率
BRAIN_LOSS_CRITIC_COEF = 0.5        # クリティック側の損失関数の重み係数
BRAIN_LOSS_ENTROPY_COEF = 0.1       # クリティック側の損失関数の重み係数
BRAIN_ADVANTAGE_SOFTPLUS = False    # アドバンテージ関数の softplus 化の有無
BRAIN_CLIPPING_MAX_GRAD = 0.5       # クリッピングする最大勾配値


def main():
    """
	強化学習の学習環境用の倒立振子課題 CartPole
    ・エージェントの行動方策の学習ロジックは、A2C [Advantage Actor Critic]
    """
    print("Start main()")
    
    # バージョン確認
    print( "OpenAI Gym", gym.__version__ )
    print( "PyTorch :", torch.__version__ )

    np.random.seed(8)
    random.seed(8)
    torch.manual_seed(8)

    #===================================
    # 学習環境、エージェント生成フェイズ
    #===================================
    # OpenAI-Gym の ENV を作成
    env = gym.make( RL_ENV )
    env.seed(8)

    #-----------------------------------
    # Academy の生成
    #-----------------------------------
    academy = CartPoleA2CAcademy( 
        env = env, 
        max_episode = NUM_EPISODE, 
        max_time_step = NUM_TIME_STEP,
        k_step = NUM_KSTEP,
        save_step = NUM_EPISODE
    )

    #-----------------------------------
    # Brain の生成
    #-----------------------------------
    brain = CartPoleA2CBrain(
        n_states = env.observation_space.shape[0],
        n_actions = env.action_space.n,
        gamma = BRAIN_GAMMDA,
        learning_rate = BRAIN_LEARNING_RATE,
        n_kstep = NUM_KSTEP,
        loss_critic_coef = BRAIN_LOSS_CRITIC_COEF,
        loss_entropy_coef = BRAIN_LOSS_ENTROPY_COEF,
        clipping_max_grad = BRAIN_CLIPPING_MAX_GRAD
    )
    
    # モデルの構造を定義する。
    brain.model()

    # 損失関数を設定する。
    #brain.loss()

    # モデルの最適化アルゴリズムを設定
    brain.optimizer()

    #-----------------------------------
	# Agent の生成
    #-----------------------------------
    agent = CartPoleAgent(
        env = env,
        brain = brain,
        gamma = BRAIN_GAMMDA
    )

    # Agent の Brain を設定
    agent.set_brain( brain )

    # 学習環境に作成したエージェントを追加
    academy.add_agent( agent )
    
    agent.print( "after init()" )
    brain.print( "after init()" )

    #===================================
    # エピソードの実行
    #===================================
    academy.academy_run()
    agent.print( "after run" )
    brain.print( "after run" )

    #===================================
    # 学習結果の描写処理
    #===================================
    #---------------------------------------------
    # 利得の履歴の plot
    #---------------------------------------------
    reward_historys = agent.get_reward_historys()

    plt.clf()
    plt.plot(
        range( len(reward_historys) ), reward_historys,
        label = 'gamma = {}'.format(BRAIN_GAMMDA),
        linestyle = '-',
        linewidth = 0.5,
        color = 'black'
    )
    plt.title( "Reward History" )
    plt.xlim( 0, NUM_EPISODE+1 )
    #plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.legend( loc = "lower right" )
    plt.tight_layout()

    plt.savefig( "{}_Reward_episode{}.png".format( RL_ENV, NUM_EPISODE), dpi = 300, bbox_inches = "tight" )
    plt.show()

    #-----------------------------------
    # 損失関数の plot
    #-----------------------------------
    loss_historys = agent.get_loss_historys()

    plt.clf()
    plt.plot(
        range( len(loss_historys) ), loss_historys,
        label = 'loss_total',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )
    plt.title( "loss" )
    plt.legend( loc = 'best' )
    plt.xlim( 0, NUM_EPISODE+1 )
    #plt.ylim( [0, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()
    plt.savefig( "{}_Loss_episode{}.png".format( academy._env.spec.id, NUM_EPISODE ), dpi = 300, bbox_inches = "tight" )
    plt.show()

    print("Finish main()")
    return

    
if __name__ == '__main__':
     main()


