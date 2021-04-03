import tensorflow as tf


try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()   # TPU Detection
    print("Found TPU")
except:
    tpu = None

if tpu:
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
else:
    strategy = tf.distribute.get_strategy()

print("REPLICAS: ", strategy.num_replicas_in_sync)

# Use tfrecord composed of a bunch of images (samples)
# inside strategy.scope()
with strategy.scope():
    # build, complile, train, predict in this scope
    pass

