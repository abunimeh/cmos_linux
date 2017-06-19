"""
Author: Guanyu Yi @ CPU Verification Platform Group
Email: yigy@cpu.com.cn
Description: pj doc sub cmd entrence
"""

import os
import shutil
import subprocess
import pcom
import env_booter

LOG = pcom.gen_logger(__name__)

def run_doc(args):
    """to run doc sub cmd"""
    if not shutil.which("NaturalDocs"):
        raise Exception("NaturalDocs is not loaded")
    if args.doc_module and args.doc_gen:
        ced, _ = env_booter.EnvBooter().module_env(args.doc_module)
        os.makedirs(ced["MODULE_DOC"], exist_ok=True)
        doc_str = "NaturalDocs -i ${PROJ_MODULE} -o HTML ${MODULE_DOC} -p ${MODULE_DOC}"
        subprocess.run(doc_str, shell=True)
        LOG.info("generating docs of module %s done", args.doc_module)
    elif args.doc_path and args.doc_gen:
        if not os.path.isdir(args.doc_path):
            raise Exception(f"doc path {args.doc_path} is NA")
        doc_dir = f"{args.doc_path}{os.sep}doc"
        os.makedirs(doc_dir, exist_ok=True)
        doc_str = f"NaturalDocs -i {args.doc_path} -o HTML {doc_dir} -p {doc_dir}"
        subprocess.run(doc_str, shell=True)
        LOG.info("generating docs of path %s done", args.doc_path)
    else:
        raise Exception("missing main arguments")
