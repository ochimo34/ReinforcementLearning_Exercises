# -*- coding:utf-8 -*-
# Anaconda 5.0.1 環境

import numpy as np
import matplotlib.pyplot as plt
import random

from matplotlib import animation

# 自作モジュール
from Academy import Academy
from MazeAcademy import MazeAcademy
from Brain import Brain
from MazeSarsaBrain import MazeSarsaBrain
from Agent import Agent
from MazeAgent import MazeAgent

# 設定可能な定数
NUM_EPISODE = 100           # エピソード試行回数
NUM_TIME_STEP = 500         # １エピソードの時間ステップの最大数
AGANT_NUM_STATES = 8        # 状態の要素数（s0~s7）※ 終端状態 s8 は除いた数
AGANT_NUM_ACTIONS = 4       # 行動の要素数（↑↓→←）
AGENT_INIT_STATE = 0        # 初期状態の位置 0 ~ 8
BRAIN_LEARNING_RATE = 0.1   # 学習率
BRAIN_GREEDY_EPSILON = 0.5  # ε-greedy 法の ε 値
BRAIN_GAMMDA = 0.99         # 割引率


def main():
    """
	強化学習の学習環境用の迷路探索問題
    ・エージェントの行動方策の学習ロジックは、Sarsa
    """
    print("Start main()")

    np.random.seed(1)
    random.seed(1)

    #===================================
    # 学習環境、エージェント生成フェイズ
    #===================================
    #-----------------------------------
    # Academy の生成
    #-----------------------------------
    academy = MazeAcademy( max_episode = NUM_EPISODE, max_time_step = NUM_TIME_STEP, save_step = 5 )

    #-----------------------------------
    # Brain の生成
    #-----------------------------------
    # 行動方策のためのパラメーターを表形式（行：状態 s、列：行動 a）で定義
    # ※行動方策を表形式で実装するために、これに対応するパラメーターも表形式で実装する。
    # 進行方向に壁があって進めない様子を表現するために、壁で進めない方向には `np.nan` で初期化する。
    # 尚、状態 s8 は、ゴール状態で行動方策がないため、これに対応するパラメーターも定義しないようにする。
    brain_parameters = np.array(
        [   # a0="Up", a1="Right", a3="Down", a4="Left"
            [ np.nan, 1,        1,         np.nan ], # s0
            [ np.nan, 1,        np.nan,    1 ],      # s1
            [ np.nan, np.nan,   1,         1 ],      # s2
            [ 1,      1,        1,         np.nan ], # s3
            [ np.nan, np.nan,   1,         1 ],      # s4
            [ 1,      np.nan,   np.nan,    np.nan ], # s5
            [ 1,      np.nan,   np.nan,    np.nan ], # s6
            [ 1,      1,        np.nan,    np.nan ], # s7
        ]
    )

    brain = MazeSarsaBrain(
        n_states = AGANT_NUM_STATES,
        n_actions = AGANT_NUM_ACTIONS,
        brain_parameters = brain_parameters,
        epsilon = BRAIN_GREEDY_EPSILON,
        gamma = BRAIN_GAMMDA,
        learning_rate = BRAIN_LEARNING_RATE
    )

    #-----------------------------------
	# Agent の生成
    #-----------------------------------
    agent = MazeAgent(
        brain = brain,
        gamma = BRAIN_GAMMDA,
        state0 = AGENT_INIT_STATE
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
    agent.print( "after simulation" )
    brain.print( "after simulation" )

    #===================================
    # 学習結果の描写処理
    #===================================
    #---------------------------------------------
    # 利得の履歴の plot
    #---------------------------------------------
    reward_historys = agent.get_reward_historys()
    plt.clf()
    plt.plot(
        range(0,NUM_EPISODE+1), reward_historys,
        label = 'gamma = {}'.format(BRAIN_GAMMDA),
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )
    plt.title( "Reward History" )
    plt.xlim( 0, NUM_EPISODE+1 )
    #plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.legend( loc = "lower right" )
    plt.tight_layout()

    plt.savefig( "MazaSimple_Sarsa_Reward_episode{}.png".format(NUM_EPISODE), dpi = 200, bbox_inches = "tight" )
    plt.show()
    
    #---------------------------------------------
    # 状態 s0 ~ s7 での状態価値関数の値を plot
    # ※ 状態 s8 は、ゴール状態で行動方策がないため、これに対応する状態価値関数も定義されない。
    #---------------------------------------------
    # 各エピソードでの状態価値関数
    v_function_historys = agent.get_v_function_historys()
    
    # list<ndarray> / shape=[n_episode,n_state] 
    # → list[ndarray] / shape = [n_episode,]
    v_function_historys_s0 = []
    v_function_historys_s1 = []
    v_function_historys_s2 = []
    v_function_historys_s3 = []
    v_function_historys_s4 = []
    v_function_historys_s5 = []
    v_function_historys_s6 = []
    v_function_historys_s7 = []
    v_function_historys_s8 = []

    for v_function in v_function_historys :
        v_function_historys_s0.append( v_function[0] )
        v_function_historys_s1.append( v_function[1] )
        v_function_historys_s2.append( v_function[2] )
        v_function_historys_s3.append( v_function[3] )
        v_function_historys_s4.append( v_function[4] )
        v_function_historys_s5.append( v_function[5] )
        v_function_historys_s6.append( v_function[6] )
        v_function_historys_s7.append( v_function[7] )
        v_function_historys_s8.append( 0 )

    plt.clf()

    # S0
    plt.subplot( 3, 3, 1 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s0,
        label = 'S0',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )
    plt.title( "V functions / S0" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S1
    plt.subplot( 3, 3, 2 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s1,
        label = 'S1',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )
    plt.title( "V functions / S1" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S2
    plt.subplot( 3, 3, 3 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s2,
        label = 'S2',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S2" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S3
    plt.subplot( 3, 3, 4 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s3,
        label = 'S3',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S3" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S4
    plt.subplot( 3, 3, 5 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s4,
        label = 'S4',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S4" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()
    
    # S5
    plt.subplot( 3, 3, 6 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s5,
        label = 'S5',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )
    plt.title( "V functions / S5" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S6
    plt.subplot( 3, 3, 7 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s6,
        label = 'S6',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S6" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    # S7
    plt.subplot( 3, 3, 8 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s7,
        label = 'S7',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S7" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()
    
    # S8
    plt.subplot( 3, 3, 9 )
    plt.plot(
        range(0,NUM_EPISODE+1), v_function_historys_s8,
        label = 'S8',
        linestyle = '-',
        #linewidth = 2,
        color = 'black'
    )

    plt.title( "V functions / S8" )
    plt.xlim( 0, NUM_EPISODE+1 )
    plt.ylim( [-0.1, 1.05] )
    plt.xlabel( "Episode" )
    plt.grid()
    plt.tight_layout()

    plt.savefig( "MazaSimple_Sarsa_VFunction_episode{}.png".format(NUM_EPISODE), dpi = 300, bbox_inches = "tight" )
    plt.show()


    #---------------------------------------------
    # 行動価値関数を plot
    #---------------------------------------------
    Q_function_historys = agent.get_q_function_historys()
    Q_function = Q_function_historys[-1]

    def draw_q_function( q_func ):
        """
        Q関数をグリッド上に分割したヒータマップで描写する。
        |　|↑　|　|
        |←|平均|→|
        |　|↓|　|
        """
        import matplotlib.cm as cm  # color map

        n_row = 3   # Maze の行数
        n_col = 3   # Maze の列数
        n_qrow = n_row * 3
        n_qcol = n_col * 3
        q_draw_map = np.zeros( shape = (n_qrow,n_qcol) )

        for i in range( n_row ):
            for j in range( n_col ):
                k = i * n_row + j   # 状態の格子番号
            
                if( k == 8 ):
                    break

                _i = 1 + ( n_row - 1 - i ) * 3
                _j = 1 + j * 3
                q_draw_map[_i][_j-1] = q_func[k][3]     # Left
                q_draw_map[_i-1][_j] = q_func[k][2]     # Down
                q_draw_map[_i][_j+1] = q_func[k][1]     # Right
                q_draw_map[_i+1][_j] = q_func[k][0]     # Up
                q_draw_map[_i][_j] = np.mean( q_func[k] )

        q_draw_map = np.nan_to_num(q_draw_map)
        #print( "q_draw_map :", q_draw_map )

        fig = plt.figure()
        ax = fig.add_subplot( 1,1,1 )
        plt.imshow(
            q_draw_map,
            cmap = cm.RdYlGn,
            interpolation = "bilinear",
            vmax = abs( q_draw_map ).max(),
            vmin = -abs( q_draw_map ).max()
        )

        plt.colorbar()
        ax.set_xlim( -0.5, n_qcol - 0.5 )
        ax.set_ylim( -0.5, n_qrow - 0.5 )
        ax.set_xticks( np.arange(-0.5, n_qcol, 3) )
        ax.set_yticks( np.arange(-0.5, n_qrow, 3) )
        #ax.set_xticklabels( range(n_col+1) )
        #ax.set_yticklabels( range(n_row+1) )
    
        # 壁を描く
        ax.plot([1*n_col-0.5, 1*n_row-0.5], [0*n_col-0.5, 1*n_row-0.5], color='black', linewidth=2)
        ax.plot([1*n_col-0.5, 2*n_row-0.5], [2*n_col-0.5, 2*n_row-0.5], color='black', linewidth=2)
        ax.plot([2*n_col-0.5, 2*n_row-0.5], [2*n_col-0.5, 1*n_row-0.5], color='black', linewidth=2)
        ax.plot([2*n_col-0.5, 3*n_row-0.5], [1*n_col-0.5, 1*n_row-0.5], color='black', linewidth=2)

        # 状態を示す文字S0～S8を描く
        ax.text(0.5*n_col-0.5, 2.5*n_row-0.5, 'S0', size=14, ha='center')
        ax.text(0.5*n_col-0.5, 2.3*n_row-0.5, 'START', ha='center')
        ax.text(0.5*n_col-0.5, 2.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(1.5*n_col-0.5, 2.5*n_row-0.5, 'S1', size=14, ha='center')
        ax.text(1.5*n_col-0.5, 2.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(2.5*n_col-0.5, 2.5*n_row-0.5, 'S2', size=14, ha='center')
        ax.text(2.5*n_col-0.5, 2.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(0.5*n_col-0.5, 1.5*n_row-0.5, 'S3', size=14, ha='center')
        ax.text(0.5*n_col-0.5, 1.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(1.5*n_col-0.5, 1.5*n_row-0.5, 'S4', size=14, ha='center')
        ax.text(1.5*n_col-0.5, 1.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(2.5*n_col-0.5, 1.5*n_row-0.5, 'S5', size=14, ha='center')
        ax.text(2.5*n_col-0.5, 1.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(0.5*n_col-0.5, 0.5*n_row-0.5, 'S6', size=14, ha='center')
        ax.text(0.5*n_col-0.5, 0.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(1.5*n_col-0.5, 0.5*n_row-0.5, 'S7', size=14, ha='center')
        ax.text(1.5*n_col-0.5, 0.1*n_row-0.5, 'reward : -0.01', ha='center')
        ax.text(2.5*n_col-0.5, 0.5*n_row-0.5, 'S8', size=14, ha='center')
        ax.text(2.5*n_col-0.5, 0.3*n_row-0.5, 'GOAL', ha='center')
        ax.text(2.5*n_col-0.5, 0.1*n_row-0.5, 'reward : +1.0', ha='center')

        # 軸を消す
        plt.tick_params(
            axis='both', which='both', bottom='off', top='off',
            labelbottom='off', right='off', left='off', labelleft='off'
        )

        ax.grid( which = "both" )
        plt.title( "Q function" )
        plt.savefig( "MazaSimple_Sarsa_Qfunction_episode{}.png".format(NUM_EPISODE), dpi = 200, bbox_inches = "tight" )
        plt.show()

        return

    draw_q_function( Q_function )

    print("Finish main()")
    return

    
if __name__ == '__main__':
     main()


