# -*- coding:utf-8 -*-
# Anaconda 5.0.1 環境

"""
    更新情報
    [19/03/18] : 新規作成
    [xx/xx/xx] : 
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os.path
from tqdm import tqdm

# 自作クラス
from Academy import Academy
from Agent import Agent


class GymAcademy( Academy ):
    """
    OpenAI Gym を利用したエージェントの強化学習環境
    
    [public]

    [protected] 変数名の前にアンダースコア _ を付ける
        _env : OpenAIGym の ENV
        
    [private] 変数名の前にダブルアンダースコア __ を付ける（Pythonルール）

    """
    def __init__( self, env, max_episode = 1, max_time_step = 100, save_step = 100 ):
        super().__init__( max_episode, max_time_step, save_step )
        self._env = env
        return


    def academy_reset( self ):
        """
        学習環境をリセットする。
        ・エピソードの開始時にコールされる
        """
        if( self._agents != None ):
            for agent in self._agents:
                agent.agent_reset()        

        self._done = False
        #self._env.reset()
        return

    def academy_run( self ):
        """
        学習環境を実行する
        """
        total_times_step = 0
        # エピソードを試行
        for episode in tqdm( range( 0, self._max_episode ), desc = "Episode" ):
            # 学習環境を RESET
            self.academy_reset()

            # 時間ステップを 1ステップづつ進める
            for time_step in range( 0 ,self._max_time_step ):
                #print( "time_step :", time_step )
                dones = []

                if( episode % self._save_step == 0 ):
                    # 学習環境の動画のフレームを追加
                    self.add_frame( episode, time_step, total_times_step )
                if( episode == self._max_episode -1 ):
                    # 学習環境の動画のフレームを追加
                    self.add_frame( episode, time_step, total_times_step )

                for agent in self._agents:
                    done = agent.agent_step( episode, time_step, total_times_step )
                    dones.append( done )

                total_times_step += 1

                # 全エージェントが完了した場合
                if( all(dones) == True ):
                    break

            # Academy と全 Agents のエピソードを完了
            self._done = True
            for agent in self._agents:
                agent.agent_on_done( episode, time_step, total_times_step )

            # 動画を保存
            if( episode % self._save_step == 0 ):
                self.save_frames( "RL_ENV_{}_Episode{}.gif".format(self._env.spec.id, episode) )
                #self.save_frames( "RL_ENV_{}_Episode{}_ts{}.gif".format(self._env.spec.id, episode, time_step) )
                self._frames = []

            if( episode == self._max_episode -1 ):
                self.save_frames( "RL_ENV_{}_Episode{}.gif".format(self._env.spec.id, episode) )
                #self.save_frames( "RL_ENV_{}_Episode{}_ts{}.gif".format(self._env.spec.id, episode, time_step) )
                self._frames = []

        return


    def add_frame( self, episode, times_step, total_times_step ):
        """
        強化学習環境の１フレームを追加する
        [Args]
            episode : <int> 現在のエピソード数
            time_step : <int> 現在のエピソードにおける経過時間ステップ数
            total_time_step : <int> 全てのエピソードにおける全経過時間ステップ数
        """
        frame = self._env.render( mode='rgb_array' )
        self._frames.append( frame )

        return


    def save_frames( self, file_name ):
        """
        外部ファイルに動画を保存する。
        """
        plt.clf()
        plt.figure(
            figsize=( self._frames[0].shape[1]/72.0, self._frames[0].shape[0]/72.0 ),
            dpi=72
        )
        patch = plt.imshow( self._frames[0] )
        plt.axis('off')
        
        def animate(i):
            patch.set_data( self._frames[i] )

        anim = animation.FuncAnimation(
                   plt.gcf(), 
                   animate, 
                   frames = len( self._frames ),
                   interval=50
        )

        # 動画の保存
        ftitle, fext = os.path.splitext(file_name)
        if( fext == ".gif" ):
            anim.save( file_name, writer = 'imagemagick' )
        else:
            anim.save( file_name )

        plt.close()

        return
