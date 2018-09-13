# -*- coding: utf-8 -*-

def reader(name):

    def getter(instance):
        return instance.__dict__[name]

    return property(getter)


def writer(name):

    def getter(instance):
        return instance.__dict__[name]

    def setter(instance, val):
        instance.__dict__[name] = val

    return property(getter, setter)


def all(name):

    def getter(instance):
        return instance.__dict__[name]

    def setter(instance, val):
        instance.__dict__[name] = val

    def deleter(instance):
        del instance.__dict__[name]

    return property(getter, setter, deleter)
