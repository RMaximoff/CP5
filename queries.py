insert_employers_query = """INSERT INTO employers (employer_id, 
                                                    company_name, 
                                                    hh_url,
                                                    company_url,
                                                    description) 
                             VALUES (%(employer_id)s, 
                                        %(company_name)s, 
                                        %(hh_url)s, 
                                        %(company_url)s, 
                                        %(description)s)
                             ON CONFLICT (employer_id) DO NOTHING"""

insert_vacancies_query = """INSERT INTO vacancies (vacancy_id, 
                                            employer_id, 
                                            vacancy_name,
                                            requirement,
                                            responsibility,
                                            salary_from,
                                            salary_to,
                                            salary_currency,
                                            url) 
                             VALUES (%(vacancy_id)s, 
                                        %(employer_id)s, 
                                        %(vacancy_name)s, 
                                        %(requirement)s, 
                                        %(responsibility)s, 
                                        %(salary_from)s, 
                                        %(salary_to)s, 
                                        %(salary_currency)s, 
                                        %(url)s)
                             ON CONFLICT (vacancy_id) DO NOTHING"""