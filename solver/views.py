# -*- coding: utf-8 -*-

import re
import operator
from sympy import Matrix
from sympy.solvers.solvers import solve_linear_system_LU
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def solve(request):
    context = {}
    if 'equations' in request.POST:

        #parse systems
        error, variables_list, equations_variables = _get_variables(request.POST['equations'])

        if error:
            context['error'] = error
            return render(request, 'index.html', context)

        vector = []
        for equation in equations_variables:
            
            #add free term if it doesn't exist
            if u'' not in equation:
                equation[u''] = 0

            for var in variables_list:
                if not var in equation:
                    equation[var] = 0
            equation_sorted = sorted(equation.iteritems(), key=operator.itemgetter(0), reverse=True)

            temp_vector = [var[1] for var in equation_sorted]

            vector.append(temp_vector)

        system = Matrix(vector)
        try:
            context['result'] = solve_linear_system_LU(system, variables_list)
        except:
            context['error'] = u'System not valid'

    return render(request, 'index.html', context)


def _get_variables(equations):
    variables_list = []
    equations_variables = []
    error = ''

    if re.findall(r'\(|\)+', equations):
        return u"Please open the brackets in the expressions and try again", variables_list, equations_variables

    if re.findall(r'[A-D]+|[F-Z]+]', equations):
        return u"Please use only lowercase letter for variable and try again", variables_list, equations_variables

    #separate of each equation
    equations = re.split(r'[^ \-+*/=.,\w\d]+', equations)

    for equation in equations:
        equation = equation.replace(' ', '')

        #for better split replace some coefficients
        equation = equation.replace('E-', 'N').replace('E+', 'P')

        variables = re.split(r'=', equation)

        if not len(variables) == 2:
            return u'Invalid data ("=")', variables_list, equations_variables

        #get variables at the left-side of equation
        left_variables = _get_equation_terms(variables[0], r'[\+]+', r'[\-]+')

        #get variables at the right-side of equation and replace it to the left-side
        if not variables[1][0] == '-':
            variables[1] = u'+%s' % variables[1]
        left_variables += _get_equation_terms(variables[1], r'[\-]+', r'[\+]+')

        #split each summand onto variable and coefficient
        variable_dict = {}
        for left_var in left_variables:
            #back previous replacement
            left_var = left_var.replace('N', 'E-').replace('P', 'E+')

            variable = re.match(r'(?P<var_value>-?\d*([.,]\d*((E)(-|\+))?)?[\d]*)?[* ]?(?P<var>[a-z]?\d*)', left_var)

            if variable.group('var') in variable_dict:
                variable_dict[variable.group('var')] += _convert_to_float(variable.group('var'), variable.group('var_value'))
            else:
                variable_dict[variable.group('var')] = _convert_to_float(variable.group('var'), variable.group('var_value'))

            if not variable.group('var') in variables_list and variable.group('var'):
                variables_list.append(variable.group('var'))

        equations_variables.append(variable_dict)

    return error, variables_list, equations_variables


def _get_equation_terms(variables, operand1, operand2):
    left_variables = []
    temp_variables = re.split(operand1, variables)

    #make proper variables negative
    for left_var in temp_variables:
        temp = re.split(operand2, left_var)
        if temp[0]:
            left_variables.append(temp[0])
        if len(temp) > 1:
            for t in temp[1:]:
                left_variables.append(u'-%s' % t)

    return left_variables


def _convert_to_float(variable, value):
    number = value
    if not variable:
        number = -float(number)
    if number == u'' or number == u'-':
        number = u'%s1' % number

    return float(number)