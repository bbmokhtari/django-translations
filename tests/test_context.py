


# class ApplyTranslationsTest(TestCase):
#     """Tests for `apply_translations`."""

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_1)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_instance_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     def test_instance_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_1, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     def test_instance_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_instance_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_instance_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_instance_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_instance_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_instance_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_prefetched_instance_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     def test_prefetched_instance_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )

#     def test_prefetched_instance_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_prefetched_instance_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_instance_invalid_entity(self):
#         class Person:
#             def __init__(self, name):
#                 self.name = name

#             def __str__(self):
#                 return self.name

#             def __repr__(self):
#                 return self.name

#         behzad = Person('Behzad')

#         with self.assertRaises(TypeError) as error:
#             apply_translations(behzad)

#         self.assertEqual(
#             error.exception.args[0],
#             ('`Behzad` is neither a model instance nor an iterable of' +
#              ' model instances.')
#         )

#     def test_instance_invalid_simple_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         europe = Continent.objects.get(code='EU')

#         with self.assertRaises(FieldDoesNotExist) as error:
#             apply_translations(europe, 'wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Continent has no field named 'wrong'"
#         )

#     def test_instance_invalid_nested_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         europe = Continent.objects.get(code='EU')

#         with self.assertRaises(FieldDoesNotExist) as error:
#             apply_translations(europe, 'countries__wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Country has no field named 'wrong'"
#         )

#     def test_instance_invalid_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         europe = Continent.objects.get(code='EU')

#         with self.assertRaises(ValueError) as error:
#             apply_translations(europe, lang='xx')

#         self.assertEqual(
#             error.exception.args[0],
#             'The language code `xx` is not supported.'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         continents = Continent.objects.all()
#         apply_translations(continents)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_1)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_queryset_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         continents = Continent.objects.all()
#         apply_translations(continents, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     def test_queryset_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_1, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     def test_queryset_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_queryset_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.all()
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_queryset_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_queryset_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_queryset_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_prefetched_queryset_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_prefetched_queryset_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     def test_prefetched_queryset_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seouler'
#         )

#     def test_prefetched_queryset_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'German'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korean'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_prefetched_queryset_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europa'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europäisch'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asien'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asiatisch'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_queryset_invalid_entity(self):
#         class Person:
#             def __init__(self, name):
#                 self.name = name

#             def __str__(self):
#                 return self.name

#             def __repr__(self):
#                 return self.name

#         people = []
#         people.append(Person('Behzad'))
#         people.append(Person('Max'))

#         with self.assertRaises(TypeError) as error:
#             apply_translations(people)

#         self.assertEqual(
#             error.exception.args[0],
#             ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
#              ' model instances.')
#         )

#     def test_queryset_invalid_simple_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         continents = Continent.objects.all()

#         with self.assertRaises(FieldDoesNotExist) as error:
#             apply_translations(continents, 'wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Continent has no field named 'wrong'"
#         )

#     def test_queryset_invalid_nested_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         continents = Continent.objects.all()

#         with self.assertRaises(FieldDoesNotExist) as error:
#             apply_translations(continents, 'countries__wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Country has no field named 'wrong'"
#         )

#     def test_queryset_invalid_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         continents = Continent.objects.all()

#         with self.assertRaises(ValueError) as error:
#             apply_translations(continents, lang='xx')

#         self.assertEqual(
#             error.exception.args[0],
#             'The language code `xx` is not supported.'
#         )


# class UpdateTranslationsTest(TestCase):
#     """Tests for `update_translations`."""

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe)

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_1)

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_2)

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_instance_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_1_2)

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2)
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )

#     def test_instance_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, lang='de')

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_instance_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_1, lang='de')

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )

#     def test_instance_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_2, lang='de')

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )

#     def test_instance_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             city_names=['cologne'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         update_translations(europe, *lvl_1_2, lang='de')

#         # reapply
#         europe = Continent.objects.prefetch_related(*lvl_1_2).get(code='EU')
#         apply_translations(europe, *lvl_1_2, lang='de')
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )

#     def test_instance_invalid_entity(self):
#         class Person:
#             def __init__(self, name):
#                 self.name = name

#             def __str__(self):
#                 return self.name

#             def __repr__(self):
#                 return self.name

#         behzad = Person('Behzad')

#         with self.assertRaises(TypeError) as error:
#             update_translations(behzad)

#         self.assertEqual(
#             error.exception.args[0],
#             ('`Behzad` is neither a model instance nor an iterable of' +
#              ' model instances.')
#         )

#     def test_instance_invalid_simple_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         europe = Continent.objects.get(code='EU')

#         with self.assertRaises(FieldDoesNotExist) as error:
#             update_translations(europe, 'wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Continent has no field named 'wrong'"
#         )

#     def test_instance_invalid_nested_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         lvl_1 = ('countries',)

#         europe = Continent.objects.prefetch_related(*lvl_1).get(code='EU')

#         with self.assertRaises(FieldDoesNotExist) as error:
#             update_translations(europe, 'countries__wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Country has no field named 'wrong'"
#         )

#     def test_instance_invalid_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         europe = Continent.objects.get(code='EU')

#         with self.assertRaises(ValueError) as error:
#             update_translations(europe, lang='xx')

#         self.assertEqual(
#             error.exception.args[0],
#             'The language code `xx` is not supported.'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_0_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents)

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_1_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_1)

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea Name'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korea Denonym'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_2)

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul Name'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seoul Denonym'
#         )

#     @override_settings(LANGUAGE_CODE='de')
#     def test_queryset_level_1_2_relation_no_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_1_2)

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2)
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea Name'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korea Denonym'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul Name'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seoul Denonym'
#         )

#     def test_queryset_level_0_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, lang='de')

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_queryset_level_1_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1 = ('countries',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_1, lang='de')

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Köln'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Kölner'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea Name'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korea Denonym'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seül'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seüler'
#         )

#     def test_queryset_level_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_2 = ('countries__cities',)
#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_2, lang='de')

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Deutschland'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Deutsche'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'Südkorea'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'Südkoreanisch'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul Name'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seoul Denonym'
#         )

#     def test_queryset_level_1_2_relation_with_lang(self):
#         create_samples(
#             continent_names=['europe', 'asia'],
#             country_names=['germany', 'south korea'],
#             city_names=['cologne', 'seoul'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             city_fields=['name', 'denonym'],
#             langs=['de', 'tr']
#         )

#         lvl_1_2 = ('countries', 'countries__cities',)

#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         # change
#         europe.name = 'Europe Name'
#         europe.denonym = 'Europe Denonym'
#         germany.name = 'Germany Name'
#         germany.denonym = 'Germany Denonym'
#         cologne.name = 'Cologne Name'
#         cologne.denonym = 'Cologne Denonym'
#         asia.name = 'Asia Name'
#         asia.denonym = 'Asia Denonym'
#         south_korea.name = 'South Korea Name'
#         south_korea.denonym = 'South Korea Denonym'
#         seoul.name = 'Seoul Name'
#         seoul.denonym = 'Seoul Denonym'
#         update_translations(continents, *lvl_1_2, lang='de')

#         # reapply
#         continents = Continent.objects.prefetch_related(*lvl_1_2)
#         apply_translations(continents, *lvl_1_2, lang='de')
#         europe = [x for x in continents if x.code == 'EU'][0]
#         germany = europe.countries.all()[0]
#         cologne = germany.cities.all()[0]
#         asia = [x for x in continents if x.code == 'AS'][0]
#         south_korea = asia.countries.all()[0]
#         seoul = south_korea.cities.all()[0]

#         self.assertEqual(
#             europe.name,
#             'Europe Name'
#         )
#         self.assertEqual(
#             europe.denonym,
#             'Europe Denonym'
#         )
#         self.assertEqual(
#             germany.name,
#             'Germany Name'
#         )
#         self.assertEqual(
#             germany.denonym,
#             'Germany Denonym'
#         )
#         self.assertEqual(
#             cologne.name,
#             'Cologne Name'
#         )
#         self.assertEqual(
#             cologne.denonym,
#             'Cologne Denonym'
#         )
#         self.assertEqual(
#             asia.name,
#             'Asia Name'
#         )
#         self.assertEqual(
#             asia.denonym,
#             'Asia Denonym'
#         )
#         self.assertEqual(
#             south_korea.name,
#             'South Korea Name'
#         )
#         self.assertEqual(
#             south_korea.denonym,
#             'South Korea Denonym'
#         )
#         self.assertEqual(
#             seoul.name,
#             'Seoul Name'
#         )
#         self.assertEqual(
#             seoul.denonym,
#             'Seoul Denonym'
#         )

#     def test_queryset_invalid_entity(self):
#         class Person:
#             def __init__(self, name):
#                 self.name = name

#             def __str__(self):
#                 return self.name

#             def __repr__(self):
#                 return self.name

#         people = []
#         people.append(Person('Behzad'))
#         people.append(Person('Max'))

#         with self.assertRaises(TypeError) as error:
#             update_translations(people)

#         self.assertEqual(
#             error.exception.args[0],
#             ('`[Behzad, Max]` is neither a model instance nor an iterable of' +
#              ' model instances.')
#         )

#     def test_queryset_invalid_simple_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         continents = Continent.objects.all()

#         with self.assertRaises(FieldDoesNotExist) as error:
#             update_translations(continents, 'wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Continent has no field named 'wrong'"
#         )

#     def test_queryset_invalid_nested_relation(self):
#         create_samples(
#             continent_names=['europe'],
#             country_names=['germany'],
#             continent_fields=['name', 'denonym'],
#             country_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         lvl_1 = ('countries',)

#         continents = Continent.objects.prefetch_related(*lvl_1)

#         with self.assertRaises(FieldDoesNotExist) as error:
#             update_translations(continents, 'countries__wrong')

#         self.assertEqual(
#             error.exception.args[0],
#             "Country has no field named 'wrong'"
#         )

#     def test_queryset_invalid_lang(self):
#         create_samples(
#             continent_names=['europe'],
#             continent_fields=['name', 'denonym'],
#             langs=['de']
#         )

#         continents = Continent.objects.all()

#         with self.assertRaises(ValueError) as error:
#             update_translations(continents, lang='xx')

#         self.assertEqual(
#             error.exception.args[0],
#             'The language code `xx` is not supported.'
#         )
