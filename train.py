import sys
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense # 通常の全結合層
from keras.layers import Flatten # データを1次元に変形
from keras.layers import Dropout # 途中のネットワークをランダムに切る
from keras.layers import Conv2D # 2D畳み込み層
from keras.layers import MaxPooling2D # プーリング層
from keras.callbacks import EarlyStopping

model = keras.models.Sequential([
  Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu', input_shape=(8, 8, 2)),
  Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  #Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  #Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  #Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu'),
  Flatten(),
  Dense(8*8, activation='softmax')
])

model.compile(
  loss=keras.losses.categorical_crossentropy,
  optimizer=keras.optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True)
)

indatas = []
outdatas = []
for l in sys.stdin:
  cols = l.strip('\r\n').split(' ')
  # 常に黒番になるように反転する
  my, your = ('2', '1') if cols[-2] == 'B' else ('1', '2')
  indatas.append(np.array(
    [int(a == my) for a in cols[:64]] + [int(a == your) for a in cols[:64]]
  ).reshape((8, 8, 2), order='F'))
  outdata = [0] * 64
  outdata[(int(cols[65])-1)*8 + int(cols[64])-1] = 1
  outdatas.append(np.array(outdata))
indatas = np.array(indatas)
outdatas = np.array(outdatas)
model.fit(indatas, outdatas, epochs=10, batch_size=512)
model.summary()

model.save(sys.argv[1] if len(sys.argv) >= 2 else 'out_model.h5')
