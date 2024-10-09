#!/bin/bash
bash neo4j.sh 
sleep 10
python extract_kw.py
python build_graph.py
python state.py

