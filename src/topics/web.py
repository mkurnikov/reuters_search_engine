from spyre import server

import matplotlib.pyplot as plt
import numpy as np

class SimpleSineApp(server.App):
    title = "LDA Topics App"
    # inputs = [{ "input_type":"text",
    #             "variable_name":"freq",
    #             "value":5,
    #             "action_id":"sine_wave_plot"}]
    inputs = [{'input_type': 'text',
               'label': 'Topics:',
               'variable_name': 'n_topics',
               'value': 5,
               'action_id': 'topics_plot'},
              {'input_type': 'text',
               'label': 'Words:',
               'variable_name': 'n_words',
               'value': 10,
               'action_id': 'topics_plot'}]

    outputs = [{"output_type":"plot",
                "output_id":"topics_plot",
                "on_page_load":True }]

    def getPlot(self, params):
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        import pickle
        import settings

        num_top_words = int(params['n_words'])
        num_of_topics = int(params['n_topics'])

        from gensim import corpora, models
        lsi = models.LdaModel.load(settings.LDA_MODEL)
        topics = lsi.show_topics(num_topics=num_of_topics, num_words=num_top_words, formatted=False)

        # print topics
        fig = plt.figure(figsize=(num_of_topics + 5, num_top_words * 0.55))
        fontsize_base = 12
        for t in range(num_of_topics):
            plt.subplot(1, num_of_topics, t + 1)
            plt.ylim(0, num_top_words + 0.5)
            plt.xticks([])
            plt.yticks([])
            plt.title('Topic #{}'.format(t + 1))
            topic_words = topics[t]
            prob_sum = sum([prob for prob, _ in topic_words])
            norm_topic_words = [(prob / prob_sum, word) for prob, word in topic_words]
            for i, (norm_prob, word) in enumerate(norm_topic_words):
                # plt.text(0.3, num_top_words - i - 0.5, word, fontsize=fontsize_base)
                plt.text(0.5, num_top_words - i - 0.5, word,
                             horizontalalignment='center',
                             # verticalalignment='center',
                             # transform = ax.transAxes,
                             fontsize=fontsize_base)


        #
        # f = float(params['freq'])
        # print f
        # x = np.arange(0,2*np.pi,np.pi/150)
        # y = np.sin(f*x)
        #
        # splt1 = fig.add_subplot(1,1,1)
        # splt1.plot(x,y)
        return fig

app = SimpleSineApp()
app.launch()