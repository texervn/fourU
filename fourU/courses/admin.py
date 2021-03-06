# -*- coding: utf-8 -*-

################################################################################
# Copyright (C) 2009 XYZ Textbooks                                             #
#                                                                              #
# This file is part of fourU.                                                  #
#                                                                              #
# This program is free software; you can redistribute it and/or modify it under#
# the terms of either: (a) the GNU General Public License as published by the  #
# Free Software Foundation; either version 3, or (at your option) any later    #
# version, or (b) the MIT License which comes with this package.               #
#                                                                              #
# fourU is distributed in the hope that it will be useful,                     #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See either the         #
# GNU General Public License or the MIT License for more details.              #
################################################################################

from django.contrib import admin
from fourU.courses.models import Course, Section, SectionEnrollment

class SectionInline(admin.StackedInline):
	model = Section
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}
	inlines = [SectionInline,]

class SectionAdmin(admin.ModelAdmin):
	list_display = ('course', 'number')

class SectionEnrollmentAdmin(admin.ModelAdmin):
	list_display = ('user', 'permissionLevel', 'course_and_section')


admin.site.register(Course, CourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(SectionEnrollment, SectionEnrollmentAdmin)
