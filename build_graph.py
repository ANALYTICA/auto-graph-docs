import neo4j
from langchain_community.graphs import Neo4jGraph
import os
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import GraphCypherQAChain
from neo4j.debug import watch
import langchain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Neo4jVector
import pickle

langchain.verbose = True
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
#os.environ["NEO4J_URI"] = "neo4j://neo4j:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"
graph = Neo4jGraph()
with open("kw_list.pkl", "rb") as f:
        kw_list = pickle.load(f)

kws = []
files = []
for entry in kw_list:
    files.append({"file":entry["file"]})
    for kw in entry["keywords"]:
        kws.append({'kw':kw[0]})
        print(kw)

merge_query = """
    MERGE(mergedKeyword:Keyword {keywordId: $keywordParam.kw})
    RETURN mergedKeyword
    """
graph.query("""
    CREATE CONSTRAINT unique_keyword IF NOT EXISTS
    FOR (k:Keyword) REQUIRE k.keywordId IS UNIQUE
    """)

for i  in range(len(kws)):
    graph.query(merge_query, params={'keywordParam':kws[i]})

cypher = cypher = """
  MATCH (k:Keyword)
  RETURN k
  """
print(graph.query(cypher))


merge_query = """
    MERGE(mergedFile:File {fileId: $fileParam.file})
    RETURN mergedFile
    """
graph.query("""
    CREATE CONSTRAINT unique_file IF NOT EXISTS
    FOR (f:File) REQUIRE f.fileId IS UNIQUE
    """)

for i  in range(len(files)):
    graph.query(merge_query, params={'fileParam':files[i]})

cypher = cypher = """
  MATCH (f:File)
  RETURN f
  """
print(graph.query(cypher))

relationship_query =  """
  MATCH (k:Keyword), (f:File)
  WHERE k.keywordId = $rParam.kw AND f.fileId = $rParam.file
  MERGE (k)-[newRelationship:KEYWORD_OF]->(f)
  RETURN count(newRelationship)
  """

 
for dic in kw_list:
#    print(dic)
    dlist = []
    for kw in dic["keywords"]:
        dlist.append({"file":dic["file"], "kw":kw[0]})
    for entry in dlist:
        graph.query(relationship_query, params={"rParam":entry})
        print(entry)


#    merge_query = """
#        MERGE(mergedChunk:Chunk {chunkId: $chunkParam.chunkId})
#        ON CREATE SET
#        mergedChunk.text = $chunkParam.text,
#        mergedChunk.embedding = $chunkParam.embedding,
#        mergedChunk.source = $chunkParam.source,
#        mergedChunk.sequence = $chunkParam.sequence
#        RETURN mergedChunk
#        """
#    graph.query("""
#        CREATE CONSTRAINT unique_chunk IF NOT EXISTS
#            FOR (c:Chunk) REQUIRE c.chunkId IS UNIQUE
#            """)

#for i  in range(len(db_chunks)):
#    graph.query(merge_query, params={'chunkParam':db_chunks[i]})

#  """
#  MATCH (s:Schedule), (i:Instructions)
#  WHERE s.name = "Schedule D" AND i.source = "if1120sd.txt"
#  MERGE (i)-[newRelationship:INSTRUCTIONS_OF]->(s)
#  RETURN count(newRelationship)
#  """


#def build_relationships():
#    for cypher in cyphers:
#        n = graph.query(cypher)
#        print("number of new relationships: ", n)
#    graph.query("""
#      CREATE VECTOR INDEX `chunked_texts` IF NOT EXISTS
#      FOR (c:Chunk) ON (c.embedding)
#      OPTIONS { indexConfig: {
#      `vector.dimensions`: 768,
#      `vector.similarity_function`: 'cosine'}}
#      """)
#    print("vector index created")
