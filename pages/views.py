# Handle the request/response logic for our web app

from django.shortcuts import render, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views.generic import TemplateView
import pickle
import pandas as pd
import os
from django.conf import settings
import pdb;


def homePageView(request):
    return render(request, 'home.html', {
        'mynumbers': [1, 2, 3, 4, 5, 6],
        'firstName': 'Min Ji',
        'lastName': 'Seo',
    })


def aboutPageView(request):
    return render(request, 'about.html')


def minjiPageView(request):
    return render(request, 'minji.html')


def homePost(request):
    # Create variable to store choice that is recognized  through entire function
    choice = -999
    gmat = -999

    try:
        # Extract value from request object by control name.
        currentChoice = request.POST['choice']
        gmatStr = request.POST['gmat']

        # print("Just before MinJi's breakpoint")
        # pdb.set_trace()
        # breakpoint()
        # print("Just after breakpoint")


        # Crude debugging effort.
        print("*** Years work experience: " + str(currentChoice))
        choice = int(currentChoice)
        gmat = float(gmatStr)

    # Enters 'except' block if integer cannot be created.
    except:
        return render(request, 'home.html', {
            'errorMessage': '*** The choice was missing please try again',
            'mynumbers': [1, 2, 3, 4, 5, 6, ]})
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', kwargs={'choice': choice, 'gmat': gmat}))


def results(request, choice, gmat):
    print("*** Inside results()")

    # Load saved model
    model_path = os.path.join(settings.BASE_DIR, 'model.pkl')

    with open(model_path, 'rb') as f:
        loadedModel = pickle.load(f)

    # Create a single prediction.
    singleSampleDF = pd.DataFrame(columns=['gmat', 'work_experience'])

    workExperience = float(choice)
    print("*** GMAT Score: " + str(gmat))
    print("*** Years Experience: " + str(workExperience))
    singleSampleDF = singleSampleDF._append({'gmat': gmat,
                                             'work_experience': workExperience},
                                            ignore_index=True)
    singlePrediction = loadedModel.predict(singleSampleDF)
    print("Single Prediction: " + str(singlePrediction))

    return render(request, 'results.html', {'choice': workExperience, 'gmat': gmat,
                                            'prediction': singlePrediction})
