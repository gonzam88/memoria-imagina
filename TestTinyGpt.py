import gpt_2_simple as gpt2

# Download the GPT-2 model (choose the desired size)
gpt2.download_gpt2(model_name="124M")

# Load the model
sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess, model_name="124M")

# Generate text using the loaded model
text = gpt2.generate(sess, model_name="124M", prefix="you are an adult filmmaker. write about your childhood memory applying cream. be specific, extensive and honest with your feeling", return_as_list=True)[0]
print(text)