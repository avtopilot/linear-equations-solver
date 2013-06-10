# -*- coding: utf-8 -*-

import re
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def solve(request):
    context = {}
    if 'equations' in request.POST:

        #separate of each equation
        equations = re.split(r'[^ \-+*/=.,\w\d]+', request.POST['equations'])

        for equation in equations:
            #TODO: check on A-Z
            equation = equation.replace(' ', '')

            #for better split replace some coefficients
            equation = equation.replace('E-', 'N').replace('E+', 'P')

            variables = re.split(r'=', equation)

            if not len(variables) == 2:
                context['error'] = u'Invalid data ("=")'
                return render(request, 'index.html', context)

            #get variables at the left-side of equation
            temp_variables = re.split(r'[\+]+', variables[0])
            left_variables = []

            #make proper variables negative
            for left_var in temp_variables:
                temp = re.split(r'[\-]+', left_var)
                left_variables.append(temp[0])
                if len(temp) > 1:
                    for t in temp[1:]:
                        left_variables.append(u'-%s' % t)

            #get variables at the right-side of equation and replace it to the left-side
            temp_variables = re.split(r'[\-]+', variables[1])

            #make proper variables negative
            for left_var in temp_variables:
                temp = re.split(r'[\+]+', left_var)
                left_variables.append(temp[0])
                if len(temp) > 1:
                    for t in temp[1:]:
                        left_variables.append(u'-%s' % t)


            for left_var in left_variables:
                #back previous replacement
                left_var = left_var.replace('N', 'E-').replace('P', 'E+')

                variable = re.match(r'(?P<var_value>-?\d*([.,]\d*((E)(-|\+))?)?[\d]*)?[* ]?(?P<var>[a-z]?\d*)', left_var)

    return render(request, 'index.html', context)