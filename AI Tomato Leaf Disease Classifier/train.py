import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("USING TENSORFLOW:", tf.__version__)

DATASET_PATH = r"train"

IMG_SIZE = (224, 224)
BATCH_SIZE = 8    # smaller batch = faster on i3
EPOCHS = 5

datagen = ImageDataGenerator(
    rescale=1/255.0,
    validation_split=0.2,
    zoom_range=0.2,
    rotation_range=20,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

print("\nLoading MobileNetV2 base model...")
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False  

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
x = Dense(64, activation='relu')(x)
output = Dense(2, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS
)

SAVE_PATH = r"leaf_classifier.h5"
print("\nSaving model to:", SAVE_PATH)
tf.keras.models.save_model(model, SAVE_PATH)

print("\nTraining Complete!")
