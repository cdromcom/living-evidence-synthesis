#!/usr/bin/env python3
"""Offline unit tests (fixture dictionaries, no network) for the decision logic.   python3 test_provenance.py"""
import json, tempfile, unittest
from pathlib import Path
import openalex, link_check, fair_checker, code_checker, data_checker, registry_check, store, run_provenance


class TestAuthorMatching(unittest.TestCase):
    def test_orcid_equal_is_confirmed(self): self.assertEqual(openalex.classify_author_match('https://orcid.org/0000-0001-6279-4158', '0000-0001-6279-4158'), 'confirmed')
    def test_orcid_different_is_other_person(self): self.assertEqual(openalex.classify_author_match('0000-0001-6279-4158', '0000-0002-1111-2222'), 'different_person')
    def test_missing_orcid_is_possible_clash(self):
        self.assertEqual(openalex.classify_author_match('0000-0001-6279-4158', None), 'possible_name_clash')
        self.assertEqual(openalex.classify_author_match(None, None), 'possible_name_clash')


class TestNoticeFilter(unittest.TestCase):
    def test_types(self):
        for t in ('letter', 'editorial', 'erratum', 'peer-review', 'retraction'): self.assertTrue(openalex.is_notice(t, 'Anything'), t)
    def test_letter_about_retraction_by_title(self):   # the Woelfle false positive: OpenAlex typed it 'article'
        self.assertTrue(openalex.is_notice('article', 'Letter Re: Retraction: Risedronate Therapy For Prevention Of Hip Fracture After Stroke In Elderly Women'))
    def test_notice_titles(self):
        for t in ('Retraction notice: X', 'Retraction: X', 'Notice of retraction', 'Expression of concern: X', 'Erratum to X', 'Correction to: X'): self.assertTrue(openalex.is_notice('article', t), t)
    def test_retracted_research_work_is_kept(self):
        self.assertFalse(openalex.is_notice('article', 'RETRACTED: A trial of something'))
        self.assertFalse(openalex.is_notice('preprint', 'Exploring the MIT Mathematics and EECS Curriculum Using Large Language Models'))


class TestTitleMatch(unittest.TestCase):
    T = 'Generative Adversarial Reviews: When LLMs Become the Critic'
    def test_exact_with_author(self):
        m = openalex.title_match(self.T, self.T, 'Bougie', ['Nicolas Bougie', 'Narimasa Watanabe']); self.assertTrue(m['accepted']); self.assertEqual(m['similarity'], 1.0)
    def test_case_and_punctuation_ignored(self):
        self.assertTrue(openalex.title_match(self.T, self.T.lower().replace(':', ''), 'bougie', ['N. Bougie'])['accepted'])
    def test_different_title_rejected(self):
        self.assertFalse(openalex.title_match(self.T, 'Generative Adversarial Networks', 'Bougie', ['Nicolas Bougie'])['accepted'])
    def test_close_title_wrong_first_author_rejected(self):
        m = openalex.title_match(self.T, self.T, 'Bougie', ['Someone Else']); self.assertFalse(m['accepted']); self.assertFalse(m['author_ok'])
    def test_arxiv_id(self):
        self.assertEqual(openalex.extract_arxiv_id('arXiv:2412.10415v2 [cs.CL] 9 Dec 2024'), '2412.10415')
        self.assertEqual(openalex.extract_arxiv_id('https://doi.org/10.48550/arXiv.2408.10365'), '2408.10365')
        self.assertIsNone(openalex.extract_arxiv_id('no id here'))


class TestAffiliations(unittest.TestCase):
    A = [{'author': {'display_name': 'A One'}, 'institutions': [{'display_name': 'OpenAI', 'type': 'company', 'country_code': 'US'}], 'raw_affiliation_strings': []},
         {'author': {'display_name': 'B Two'}, 'institutions': [{'display_name': 'Stanford University', 'type': 'education'}], 'raw_affiliation_strings': ['Meta-Research Innovation Center at Stanford (METRICS)']},
         {'author': {'display_name': 'C Three'}, 'institutions': [], 'raw_affiliation_strings': ['Meta Platforms, Menlo Park']}]
    def test_company_and_vendor(self):
        co, vh = openalex.affiliation_facts(self.A, ['OpenAI', 'Meta', 'Anthropic'])
        self.assertEqual([c['author'] for c in co], ['A One'])
        self.assertEqual(sorted((h['author'], h['vendor']) for h in vh), [('A One', 'OpenAI'), ('C Three', 'Meta')])   # Meta-Research is not Meta
    def test_published_version(self):
        w = {'locations': [{'source': {'type': 'repository', 'display_name': 'arXiv'}, 'landing_page_url': 'https://arxiv.org/abs/1'},
                           {'source': {'type': 'journal', 'display_name': 'J X'}, 'landing_page_url': 'https://doi.org/10.1/abc', 'version': 'publishedVersion'}]}
        self.assertEqual(openalex.published_versions(w, '10.48550/arxiv.1')[0]['doi'], '10.1/abc')
        self.assertEqual(openalex.published_versions({'locations': w['locations'][:1]}, '10.48550/arxiv.1'), [])


class TestLinks(unittest.TestCase):
    def test_classes(self):
        c = link_check.classify_url
        self.assertEqual(c('https://github.com/owner/repo'), 'code repository')
        self.assertEqual(c('https://github.com/owner'), 'other')
        self.assertEqual(c('https://gitlab.com/o/r'), 'code repository')
        self.assertEqual(c('https://zenodo.org/records/123'), 'data repository')
        self.assertEqual(c('https://doi.org/10.5281/zenodo.123'), 'data repository')
        self.assertEqual(c('https://huggingface.co/datasets/a/b'), 'data repository')
        self.assertEqual(c('https://huggingface.co/spaces/a/b'), 'code repository')
        self.assertEqual(c('https://clinicaltrials.gov/study/NCT01234567'), 'registry')
        self.assertEqual(c('https://www.crd.york.ac.uk/prospero/display_record.php?RecordID=1'), 'registry')
        self.assertEqual(c('https://aspredicted.org/abc.pdf'), 'registry')
        self.assertEqual(c('https://osf.io/abcde/', 'This study was preregistered'), 'registry')
        self.assertEqual(c('https://osf.io/abcde/', 'The data and materials are on OSF'), 'data repository')
        self.assertEqual(c('https://academic.oup.com/x/article-lookup/doi/10.1/y#supplement'), 'supplement')
        self.assertEqual(c('https://example.org/page'), 'other')
    def test_clean_url(self):
        self.assertEqual(link_check.clean_url('https://a.org/x).'), 'https://a.org/x')
        self.assertEqual(link_check.clean_url('https://a.org/x_(y)'), 'https://a.org/x_(y)')
    def test_join_hyphenation_and_broken_urls(self):
        j = link_check._join_broken
        self.assertEqual(j('the recommen-\ndation holds'), 'the recommendation holds')
        self.assertIn('https://doi.org/10.21203/rs.3.rs-3288515/v1', j('https://doi.org/10.21203/rs.3.rs-\n3288515/v1.\n11'))
        self.assertIn('https://ai.meta.com/blog/meta-llama-3/', j('https://ai.meta.com/blog/meta-\nllama-3/'))      # URL hyphen is kept
        self.assertNotIn('v1.11', j('https://doi.org/10.1/x/v1.\n11'))                                              # a page number is not joined
        self.assertIn('10.1016/j.jclinepi.2024.111533', j('doi.org/10.1016/j.jclinepi.2024.\n111533'))
    def test_repair_doi(self):
        self.assertEqual(link_check.repair_doi('10.1162/coli', 'ISSN 0891-2017.\ndoi: 10.1162/coli a 00524.\nChen Gao'), '10.1162/coli_a_00524')
        self.assertIsNone(link_check.repair_doi('10.1162/abc', 'doi: 10.1162/abc.\nNext'))
    def test_status(self):
        s = link_check.link_status
        self.assertEqual(s(200, None, 'https://a.org/', 'https://a.org/'), ('ok', 'ok'))
        self.assertEqual(s(404, None, 'x', 'x'), ('flag', 'dead'))
        self.assertEqual(s(403, None, 'x', 'x'), ('unavailable', 'blocked'))
        self.assertEqual(s(None, 'ConnectionError: Max retries', 'x', 'x'), ('unavailable', 'unreachable'))
        self.assertEqual(s(None, 'ConnectionError', 'x', 'x', dns_failure=True), ('flag', 'dead'))
        self.assertEqual(s(200, None, 'https://idp.example.org/login?next=1', 'https://a.org/paper'), ('flag', 'redirect-to-login'))
        self.assertEqual(s(200, None, 'x', 'x', doi_registered=False), ('flag', 'dead'))
    def test_availability_statements(self):
        t = 'Data availability. The code and data are available from the corresponding author upon reasonable request. Other text. Code will be released upon publication.'
        kinds = {s['kind'] for s in link_check.availability_statements(t)}
        self.assertEqual(kinds, {'on request', 'future release'})
        self.assertEqual(link_check.availability_statements('Samples were available on request of the clinic.'), [])   # no code/data wording


class TestFair(unittest.TestCase):
    def _res(self, mid, v): return {'@type': ['https://w3id.org/ftr#TestResult'], 'http://www.w3.org/ns/prov#value': [{'@value': v}], 'https://w3id.org/ftr#outputFromTest': [{'@id': f'https://w3id.org/fairchecker/test/{mid}'}]}
    def test_grouping(self):
        ids = ['F1A', 'F1B', 'F2A', 'F2B', 'A11', 'A12', 'I1', 'I2', 'I3', 'R11', 'R12', 'R13']
        d = [self._res(i, 2 if i.startswith('F') else 1) for i in ids] + [{'@type': ['https://w3id.org/ftr#Test']}]
        g = fair_checker.group_fair(fair_checker.parse_results(d))
        self.assertEqual((g['F']['score'], g['F']['max']), (8, 8)); self.assertEqual((g['A']['score'], g['A']['max']), (2, 4))
        self.assertEqual((g['I']['score'], g['I']['max']), (3, 6)); self.assertEqual((g['R']['score'], g['R']['max']), (3, 6)); self.assertEqual(g['metrics_without_id'], 0)
    def test_missing_ids_are_not_guessed(self):
        d = [self._res('None', 2), self._res('F1A', 2)]
        g = fair_checker.group_fair(fair_checker.parse_results(d))
        self.assertEqual(g['metrics_without_id'], 1); self.assertFalse(g['F']['complete']); self.assertIsNone(g['F']['score'])


class TestCode(unittest.TestCase):
    def test_parse_repo(self):
        self.assertEqual(code_checker.parse_repo('https://github.com/o/r.git'), ('github.com', 'o', 'r'))
        self.assertEqual(code_checker.parse_repo('https://www.github.com/o/r/tree/main/x'), ('github.com', 'o', 'r'))
        self.assertIsNone(code_checker.parse_repo('https://github.com/o'))
    def test_readme(self):
        self.assertTrue(code_checker.readme_instructions('# Tool\n\n## Installation\n\npip install x\n')['has_instructions'])
        self.assertTrue(code_checker.readme_instructions('Intro\n\n```\npython run.py\n```\n')['has_instructions'])
        self.assertTrue(code_checker.readme_instructions('1. Create folders\n2. Adjust and run script.py\n')['has_instructions'])
        self.assertFalse(code_checker.readme_instructions('# Tool\n\nAbstract only.\n')['has_instructions'])
    def test_pinning(self):
        p = code_checker.pinning
        self.assertEqual(p('requirements.txt', 'numpy==1.24\npandas==2.0\n')['state'], 'pinned')
        self.assertEqual(p('requirements.txt', '# c\nnumpy==1.24\npandas\n')['state'], 'partly pinned')
        self.assertEqual(p('requirements.txt', 'numpy\npandas>=2\n')['state'], 'not pinned')
        self.assertEqual(p('renv.lock', '{}')['state'], 'lock file')
        self.assertEqual(p('package.json', json.dumps({'dependencies': {'a': '1.2.3', 'b': '^2.0.0'}}))['state'], 'partly pinned')
        self.assertEqual(p('environment.yml', 'name: x\ndependencies:\n  - python=3.11\n  - numpy\n')['state'], 'partly pinned')
    def test_dates(self):
        d = code_checker.date_facts('2024-10-01T00:00:00Z', '2025-02-08T00:00:00Z', '2024-10-01', '2025-02-08', '2024-06-26')
        self.assertTrue(d['created_after_paper']); self.assertTrue(d['pushed_after_paper']); self.assertEqual(d['last_commit_days_after_paper'], 227); self.assertFalse(d['first_commit_before_paper'])


class TestData(unittest.TestCase):
    def test_hosts_and_pid(self):
        self.assertEqual(data_checker.host_kind('https://zenodo.org/records/1'), 'zenodo.org')
        self.assertEqual(data_checker.host_kind('https://huggingface.co/datasets/a/b'), 'huggingface.co')
        self.assertTrue(data_checker.host_kind('https://github.com/o/r').startswith('code host'))
        self.assertTrue(data_checker.host_kind('https://user.github.io/x').startswith('code host'))
        pid = data_checker.persistent_identifier('https://github.com/o/r', None); self.assertFalse(pid['has']); self.assertIn('no persistent identifier', pid['note'])
        self.assertFalse(data_checker.persistent_identifier('https://lab.example.edu/data', None)['has'])
        self.assertEqual(data_checker.find_doi('https://zenodo.org/records/3775793'), '10.5281/zenodo.3775793')
        self.assertEqual(data_checker.find_doi('https://doi.org/10.5061/dryad.abc123).'), '10.5061/dryad.abc123')
    def test_datacite_summary(self):
        s = data_checker.summarize_datacite({'rightsList': [{'rights': 'CC BY 4.0', 'rightsUri': 'https://creativecommons.org/licenses/by/4.0/legalcode', 'rightsIdentifier': 'cc-by-4.0'},
                                                            {'rights': 'Open Access', 'rightsUri': 'info:eu-repo/semantics/openAccess'}],
                                             'types': {'resourceTypeGeneral': 'Dataset'}, 'creators': [{'name': 'A, B'}], 'sizes': ['10 MB']})
        self.assertEqual(s['licence'], ['cc-by-4.0']); self.assertEqual(s['access_conditions'], ['info:eu-repo/semantics/openAccess']); self.assertEqual(s['resource_type'], 'Dataset')


class TestRegistry(unittest.TestCase):
    def test_ids(self):
        r = registry_check.find_ids('Registered as NCT01234567 and CRD42020123456; see https://osf.io/ab3cd/ and https://aspredicted.org/xy12z')
        self.assertEqual({(x['registry'], x['id']) for x in r}, {('ClinicalTrials.gov', 'NCT01234567'), ('PROSPERO', 'CRD42020123456'), ('OSF', 'ab3cd'), ('AsPredicted', 'xy12z')})
    def test_collection_years(self):
        self.assertEqual(registry_check.stated_collection_years('Data were collected in 2022 from schools.')[0]['year'], 2022)


class TestStore(unittest.TestCase):
    def test_merge_keeps_other_keys(self):
        existing = {'schema': 1, 'papers': {'k1': {'signals': {'a': 1}, 'title': 'Old', 'provenance': [{'id': 'old'}]}, 'k2': {'signals': {'b': 2}}}}
        out = store.merge_paper(existing, 'k1', [store.make_item('retraction', 'R', 'T', 'ok', 'fine')], title='New', doi='10.1/x')
        self.assertEqual(out['papers']['k1']['signals'], {'a': 1}); self.assertEqual(out['papers']['k2'], {'signals': {'b': 2}}); self.assertEqual(out['schema'], 1)
        self.assertEqual(out['papers']['k1']['title'], 'New'); self.assertEqual(out['papers']['k1']['doi'], '10.1/x'); self.assertEqual([i['id'] for i in out['papers']['k1']['provenance']], ['retraction'])
        self.assertIn('checked_utc', out['papers']['k1'])
    def test_new_paper_and_empty_store(self):
        out = store.merge_paper({}, 'k', [], title='T'); self.assertEqual(list(out['papers']), ['k']); self.assertNotIn('doi', out['papers']['k'])
    def test_write_roundtrip_does_not_clobber(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'sub' / 'q.json'; p.parent.mkdir(); p.write_text(json.dumps({'papers': {'k': {'signals': {'x': 1}}}}))
            store.write('k', [store.make_item('links', 'L', 'T', 'flag', 'r')], 'T', '10.1/y', path=p)
            data = json.loads(p.read_text()); self.assertEqual(data['papers']['k']['signals'], {'x': 1}); self.assertEqual(data['papers']['k']['provenance'][0]['status'], 'flag')
    def test_item_fields_and_status_check(self):
        it = store.make_item('a', 'b', 'c', 'ok', 'r'); self.assertEqual(set(it), {'id', 'label', 'tool', 'status', 'result', 'detail', 'url', 'checked_utc', 'http_status', 'response_sha256', 'data'})
        with self.assertRaises(AssertionError): store.make_item('a', 'b', 'c', 'maybe', 'r')


class TestWording(unittest.TestCase):
    def test_plain(self):
        self.assertNotIn('—', run_provenance.plain('a — b')); self.assertNotRegex(run_provenance.plain('The call failed and may fail'), r'(?i)\bfail')


if __name__ == '__main__': unittest.main(verbosity=1)
