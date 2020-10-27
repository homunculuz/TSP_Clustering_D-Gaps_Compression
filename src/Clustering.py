"""
   medoids: [medoid_0, .... , medoid_k ]
   medoid_i:  (doc-termsID,clusterID,docID)

   clusters: { 0: [(doc-termsID,docID)...], 1:[(doc-termsID,docID)...],...., k:[(doc-termsID,docID)...] }

    get_docs_set_terms_id(dictionary, n): given dictionary and number of documents give a set of document vectors
                                          (doc-terms) which contain the terms indexed in lexicographic order in
                                          dictionary, in growing ordering. return-> list of [(doc-termsID),docID]

    stream_cluster(sorted_collection, radius): given the set of doc-terms vector permit to obtain clusters and specific
                                               medoids

    find_medoid(medoids, doc): permit to classify selecting the minimum Jaccard Distance between medoid of
                               the clusters and  specific doc-terms.

    def distance_jaccard(doc1, doc2): permit to calculate the distance between two set, small is better for similarity.


"""

ROUND = 5  # float numbers round


def distance_jaccard(doc1, doc2):
    if doc1 and doc2:
        intersection_docs = [value for value in doc1 if value in doc2]
        return round(1 - len(intersection_docs) / (len(doc1 + doc2)), ROUND)
    else:
        return 0


def find_medoids(medoids, doc_terms):
    if not medoids:  # no clusters yet
        return 1, []
    first_medoid, cluster_id, doc_id = medoids[0]  # given
    distance = distance_jaccard(first_medoid, doc_terms), cluster_id
    for medoid, cluster_id, doc_id in medoids[1:]:  # permit to select the minimum from all distance
        new_distance = distance_jaccard(medoid, doc_terms)
        if new_distance < distance[0]:
            distance = new_distance, cluster_id
    return distance


def stream_cluster(docID_TermsID: tuple, radius):
    k = 0  # number of cluster

    medoids = []  # list of (doc-termsID,docID, clusterID)
    clusters = {}  # contain the dictionary with clusterID (0<=clusterID<=k) and values are list docs-termsID

    for doc in docID_TermsID:
        doc_terms_id, doc_id = doc
        distance, cluster_id = find_medoids(medoids, doc_terms_id)  # calculate the distance
        if distance <= radius:
            clusters[cluster_id].append(doc_id)  # add to cluster
        else:
            medoids.append((doc_terms_id, k, doc_id))  # create new cluster and medoid
            clusters[k] = []
            k += 1  # increment number of cluster
    return medoids, clusters


# return list of (doc-termsID,doc-ID)
def get_docs_set_terms_id(dictionary, n, is_reverse=True):
    list_of_terms_ids = [[] for i in range(n)]  # list of docs
    term_id = 0  # term-ID saved in the doc-terms vectors
    for term in dictionary:
        for doc_id in dictionary[term]:  # posting lists saved in the term
            list_of_terms_ids[doc_id - 1].append(term_id)  # add termID in the doc set
        term_id += 1
    docs_terms = [(list_of_terms_ids[doc_id], doc_id) for doc_id in range(n)]  # insert the docID
    if is_reverse:
        docs_terms.sort(key=lambda x: len(x[0]), reverse=is_reverse)  # ordering in reverse order length
    return docs_terms


def do_clustering(documents, n, radius):
    # create the hyper-points
    docID_Terms = get_docs_set_terms_id(documents, n)
    # check number of elements
    assert (len(docID_Terms) == n)
    return stream_cluster(docID_Terms, radius)