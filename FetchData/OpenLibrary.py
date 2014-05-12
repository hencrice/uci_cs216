import json
from urllib2 import urlopen
from urllib import urlencode
from cStringIO import StringIO
from PIL import Image
from numpy import array, float32

legalKeys=set(("title", "author", "q"))
searchBaseUrl='http://openlibrary.org/search.json?'
coverBaseUrl='http://covers.openlibrary.org/b/olid/{0}-{1}.jpg'
fieldsToKeep=('cover_edition_key', 'title', 'author_name')

def searchAndGetBookInfo(criteria, coverImgSize='M', limit=1):
    '''
    Input:
        criteria: A dictionary specifies the search criteria. Legal keys are: "title", "author", and "q" for
        general search.
        
        coverImgSize: There are 'L', 'M', 'S'.
        
        limit: When there are multiple hits for the search, how many records to return (with book cover images).
    Returns:
        numOfHits: Integer represents the number of hits of this search.
        results: List of JSONs with fields: "cover_edition_key", "title", "author_name", "cover_img"
    '''
    assert len(criteria)>0 and set(criteria.keys()) <= legalKeys, "No keys or illegal keys found in criteria"
    results=json.loads(''.join(urlopen(searchUrlBase+urlencode(criteria)).readlines()))
    numOfHits=results['numFound']
    results=results['docs']
    for i, r in enumerate(results):
        if i==limit: # got enough records
            break
        if 'cover_edition_key' not in r: # if we can't fetch book cover image, ignore this record
            continue
#         results[i]={f:r[f] if f in r else None for f in fieldsToKeep}
        results[i]={f:r[f] for f in fieldsToKeep} # remove all redundant fields
        # create numpy array from remote jpg files
        img = Image.open(StringIO(urlopen(coverBaseUrl.format(r['cover_edition_key'], coverImgSize)).read()))
        results[i]['cover_img']=array(img, float32)
    return numOfHits, results

if __name__ == '__main__':
	criteria={'title':'''Harry Potter and the Philosopher's Stone'''}
	n, results=searchAndBookInfo(criteria)
	print((n, results[0]['title'], results[0]['author_name'], results[0]['cover_img'].shape))