# A2C [Advantage Actor Critic] による倒立振子課題（CartPole）【実装中...】
強化学習の学習環境用の倒立振子課題 CartPole。<br>
ディープラーニングを用いた強化学習手法である A2C [Advantage Actor Critic] によって、単純な２次元の倒立振子課題を解く。<br>

※ ここでの A2C のネットワーク構成は、簡単のため、CNNではなく多層パーセプトロン（MLP）で代用したもので実装している。<br>

## ■ 項目 [Contents]
1. [動作環境](#動作環境)
1. [使用法](#使用法)
1. [コード説明＆実行結果](#コード説明＆実行結果)
1. 背景理論
    1. [【外部リンク】強化学習 / A2C [Advantage Actor-Critic]](https://github.com/Yagami360/My_NoteBook/blob/master/%E6%83%85%E5%A0%B1%E5%B7%A5%E5%AD%A6/%E6%83%85%E5%A0%B1%E5%B7%A5%E5%AD%A6_%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92_%E5%BC%B7%E5%8C%96%E5%AD%A6%E7%BF%92.md#A2C)


## ■ 動作環境

- Python : 3.6
- Anaconda : 5.0.1
- OpenAIGym : 0.10.9
- PyTorch : 1.0.0

## ■ 使用法

- 使用法
```
$ python main.py
```

- 設定可能な定数
```python
[main.py]
NUM_EPISODE = 500               # エピソード試行回数
NUM_TIME_STEP = 200             # １エピソードの時間ステップの最大数
BRAIN_LEARNING_RATE = 0.0001    # 学習率
BRAIN_BATCH_SIZE = 32           # ミニバッチサイズ
BRAIN_GAMMDA = 0.99             # 利得の割引率
```

<a id="コード説明＆実行結果"></a>

## ■ コード説明＆実行結果

### ◎ コードの実行結果

|パラメータ名|値（実行条件１）|値（実行条件２）|
|---|---|---|
|エピソード試行回数：`NUM_EPISODE`|500|500|
|１エピソードの時間ステップの最大数：`NUM_TIME_STEP`|200|←|
|学習率：`learning_rate`|0.0001|←|
|ミニバッチサイズ：`BRAIN_LEARNING_RATE`|32|←|
|最適化アルゴリズム|Adam|←|
|利得の割引率：`BRAIN_GAMMDA`|0.99|←|
|報酬の設定|転倒：-1<br>連続 `NUM_TIME_STEP=200`回成功：+1<br>それ以外：0|←|
|シード値|`np.random.seed(8)`<br>`random.seed(8)`<br>`torch.manual_seed(8)`<br>`env.seed(8)`|←|
|A2C のネットワーク構成|MLP（3層）<br>入力層：状態数（4）<br>隠れ層：32ノード<br>アクター側の出力層：行動数（2）<br>クリティック側の出力層：1|


- 割引利得のエピソード毎の履歴（実行条件１）<br>

- 損失関数のグラフ（実行条件１）<br>


### ◎ コードの説明


## ■ デバッグ情報

```python
[main.py]
state : tensor([ 0.0384, -0.0423,  0.0327,  0.0217])

actions : 
tensor(
[
        [[1], [0], [0], [0], [1],... [0], [0], [0]],
        [[0], [0], [0], [0],... [0], [0], [0]],
        [[0], [0], [0], [0],... [0], [0], [0]],
        [[0], [0], [0], [0],... [0], [0], [0]],
        [[0], [0], [0], [0],... [0], [0], [0]],


actor_output :
 tensor([-0.0959, -0.1605])
critic_output :
 tensor([-0.0931])
RuntimeError: Dimension out of range (expected to be in range of [-1, 0], but got 1)
```
```python
[main1_1.py]
rollouts.observations[step] : tensor([[-0.0073, -0.0234, -0.0114, -0.0126],
        [ 0.0334,  0.0239,  0.0180, -0.0110],
        [-0.0073,  0.0345, -0.0444,  0.0484],
        [ 0.0421,  0.0130, -0.0285, -0.0105],
        [-0.0427, -0.0155, -0.0044,  0.0052],
        [ 0.0062,  0.0287, -0.0027,  0.0003],
        [-0.0094, -0.0457, -0.0054,  0.0049],
        [-0.0470,  0.0334, -0.0281,  0.0020],
        [ 0.0193, -0.0001, -0.0229,  0.0381],
        [-0.0475, -0.0395, -0.0072,  0.0284],
        [ 0.0488,  0.0169,  0.0302, -0.0486],
        [ 0.0036,  0.0120,  0.0253, -0.0430],
        [-0.0361, -0.0168,  0.0114,  0.0032],
        [-0.0446,  0.0047,  0.0117, -0.0152],
        [-0.0081,  0.0055, -0.0254,  0.0139],
        [-0.0253, -0.0122, -0.0118, -0.0198],
        [-0.0144, -0.0390,  0.0422,  0.0345],
        [-0.0129,  0.0199,  0.0433, -0.0175],
        [-0.0342,  0.0321, -0.0039, -0.0184],
        [-0.0348,  0.0129,  0.0216,  0.0323],
        [-0.0484,  0.0237, -0.0317,  0.0433],
        [ 0.0404, -0.0270, -0.0444,  0.0082],
        [ 0.0055, -0.0034, -0.0487,  0.0359],
        [ 0.0397, -0.0013, -0.0277, -0.0295],
        [-0.0130, -0.0130,  0.0177,  0.0495],
        [ 0.0266,  0.0054,  0.0311, -0.0010],
        [ 0.0467,  0.0025, -0.0219,  0.0044],
        [ 0.0483, -0.0079,  0.0275, -0.0044],
        [ 0.0471, -0.0198, -0.0133, -0.0425],
        [-0.0272,  0.0193,  0.0242,  0.0500],
        [ 0.0146,  0.0409, -0.0183, -0.0178],
        [ 0.0274, -0.0419, -0.0456,  0.0396]])


actor_output :
 tensor([[ 0.0330, -0.1027],
        [ 0.0339, -0.0981],
        [ 0.0316, -0.0992],
        [ 0.0288, -0.1052],
        [ 0.0301, -0.1005],
        [ 0.0331, -0.0972],
        [ 0.0240, -0.1047],
        [ 0.0340, -0.1027],
        [ 0.0283, -0.0962],
        [ 0.0305, -0.1001],
        [ 0.0255, -0.1014],
        [ 0.0291, -0.0951],
        [ 0.0351, -0.0948],
        [ 0.0299, -0.0947],
        [ 0.0338, -0.1001],
        [ 0.0298, -0.1015],
        [ 0.0260, -0.0987],
        [ 0.0268, -0.0994],
        [ 0.0258, -0.1074],
        [ 0.0304, -0.1046],
        [ 0.0266, -0.1006],
        [ 0.0262, -0.1050],
        [ 0.0299, -0.0968],
        [ 0.0297, -0.0986],
        [ 0.0323, -0.0934],
        [ 0.0329, -0.0945],
        [ 0.0268, -0.1014],
        [ 0.0268, -0.1036],
        [ 0.0304, -0.1015],
        [ 0.0313, -0.0982],
        [ 0.0291, -0.0978],
        [ 0.0271, -0.1012]])

```

```python
----------------------------------
CartPoleA2CBrain
<AdavantageMemory.AdavantageMemory object at 0x000001A89E35A908>

_index :
 1
_observations :
 tensor([[ 0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0384, -0.0423,  0.0327,  0.0217],
        [ 0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0000],
        [ 0.0000,  0.0000,  0.0000,  0.0000]])
_rewards :
 tensor([[0.],
        [0.],
        [0.],
        [0.],
        [0.]])
_actions :
 tensor([[1],
        [0],
        [0],
        [0],
        [0]])
_done_masks :
 tensor([[0.],
        [1.],
        [0.],
        [0.],
        [0.],
        [0.]])
_total_rewards :
 tensor([[ 0.0000],
        [ 0.0000],
        [ 0.0000],
        [ 0.0000],
        [-0.0931]])
----------------------------------
```
```python
------------------------------------
index : 0
observations :
 tensor([[[ 0.0069,  0.0397,  0.0118,  0.0145]],

        [[ 0.0076, -0.1556,  0.0121,  0.3109]],

        [[ 0.0045, -0.3509,  0.0183,  0.6073]],

        [[-0.0025, -0.1561,  0.0304,  0.3205]],

        [[-0.0056,  0.0386,  0.0368,  0.0375]],

        [[-0.0048,  0.2332,  0.0376, -0.2433]]])
rewards :
 tensor([[[0.]],

        [[0.]],

        [[0.]],

        [[0.]],

        [[0.]]])
actions :
 tensor([[[0]],

        [[0]],

        [[1]],

        [[1]],

        [[1]]])
masks :
 tensor([[[1.]],

        [[1.]],

        [[1.]],

        [[1.]],

        [[1.]],

        [[1.]]])
returns :
 tensor([[[ 0.0000]],

        [[ 0.0000]],

        [[ 0.0000]],

        [[ 0.0000]],

        [[ 0.0000]],

        [[-0.1561]]])
------------------------------------

```