import streamlit as st
import os
import torch
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, PromptTemplate
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.postprocessor import SimilarityPostprocessor

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="MPK AI Assistant - Ultra Mode", layout="wide")

# --- SIDEBAR: PENGATURAN & RIWAYAT ---
with st.sidebar:
    st.header("⚙️ System Settings")
    
    selected_lang = st.radio(
        "Response Language:",
        ["Bahasa Indonesia", "English"],
        index=0,
        help="Pilihan Bahasa AI."
    )
    
    st.divider()
    st.header("💬 Chat History")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                short_text = (msg["content"][:25] + '...') if len(msg["content"]) > 25 else msg["content"]
                st.write(f"{i//2 + 1}. {short_text}")
    
    st.divider()
    if st.session_state.messages:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 Download Log Audit", chat_text, "audit_log.txt", use_container_width=True)

    if st.button("🗑️ Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 2. Setup Mesin AI (DIOPTIMASI UNTUK RTX 4050)
@st.cache_resource
def setup_settings():
    # Setting LLM dengan parameter "Seimbang"
    Settings.llm = Ollama(
        model="MPK-AI", 
        request_timeout=600.0, 
        additional_kwargs={
            "temperature": 0.1,    # Kaku biar akurat
            "top_p": 0.85,         # Tetap natural
            "top_k": 20,           # Fokus pada jawaban teknis
            "num_gpu": 35,         # PAKSA PAKAI RTX 4050
            "num_thread": 8        # Optimasi CPU
        }
    )
    # Embedding tetap di CUDA agar indexing cepat
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5",
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    return True

setup_settings()

st.title("MPK AI Assistant")
st.markdown("##### Prototype Grade A System | IT Intern Team PT MPK")
st.divider()

# 3. Load & Indexing Dokumen
@st.cache_resource
def load_index():
    if not os.path.exists("./data"): return None
    try:
        # SimpleDirectoryReader otomatis ambil metadata file & page
        documents = SimpleDirectoryReader(input_dir="./data", recursive=True).load_data()
        return VectorStoreIndex.from_documents(documents) if documents else None
    except Exception as e:
        st.error(f"Error indexing: {e}")
        return None

index = load_index()

if index:
    # HARD-LOCK LANGUAGE LOGIC
    if selected_lang == "Bahasa Indonesia":
        lang_instr = "WAJIB MENJAWAB DALAM BAHASA INDONESIA."
        no_data_msg = "Data tidak ditemukan dalam dokumen resmi MPK."
    else:
        lang_instr = "YOU MUST ANSWER IN ENGLISH ONLY."
        no_data_msg = "Data not found in MPK official documents."

    # PROMPT TEMPLATE (DIPERKETAT)
    qa_prompt_str = (
        f"CRITICAL INSTRUCTION: {lang_instr}\n\n"
        "SYSTEM ROLE: You are MPK-AI, a professional audit assistant for PT MPK.\n"
        "REFERENCE CONTEXT:\n{context_str}\n"
        "---------------------\n"
        "STRICT SOP:\n"
        "1. DISTINGUISH: Refizal, SH is the NOTARY, NOT the owner.\n"
        "2. SOURCES: Priority to '20251017_Company Profile_PT Mopakha.pdf'.\n"
        "3. TRUTH: Only answer based on context. Do not hallucinate.\n"
        f"4. OUTPUT: Regardless of the question language, {lang_instr}\n\n"
        "Question: {query_str}\n"
        "MPK-AI Answer: "
    )
    
    # QUERY ENGINE SEIMBANG (Tanpa HyDE agar tidak lemot)
    query_engine = index.as_query_engine(
        streaming=True,
        similarity_top_k=5, # Ambil 5 potongan terbaik
        text_qa_template=PromptTemplate(qa_prompt_str),
        node_postprocessors=[
            SimilarityPostprocessor(similarity_cutoff=0.60) # Hanya ambil yang akurasi > 80%
        ]
    )

    # 4. Chat UI
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Tanyakan apa saja tentang MPK..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_response = ""
            
            try:
                # Tambahkan instruksi bahasa "invisible"
                final_query = f"{prompt}. (Answer in {selected_lang})"
                response = query_engine.query(final_query)
                
                # Cek apakah ada data di source_nodes
                if not response.source_nodes:
                    full_response = no_data_msg
                else:
                    for text in response.response_gen:
                        full_response += text
                        resp_placeholder.markdown(full_response + "▌")
                    
                    # --- FITUR KROSCEK TIM AUDIT (FILE + HALAMAN) ---
                    if "tidak ditemukan" not in full_response.lower() and "not found" not in full_response.lower():
                        source_details = []
                        for n in response.source_nodes:
                            fname = n.node.metadata.get('file_name', 'Unknown')
                            page = n.node.metadata.get('page_label', '?')
                            source_details.append(f"{fname} (Hal. {page})")
                        
                        # Hapus duplikat
                        unique_sources = list(set(source_details))
                        label = "Sumber Data" if selected_lang == "Bahasa Indonesia" else "Sources"
                        
                        full_response += f"\n\n---\n**{label}:**\n"
                        for s in unique_sources:
                            full_response += f"- `{s}`\n"
                
                resp_placeholder.markdown(full_response)
            except Exception as e:
                full_response = f"System Error: {e}"
                resp_placeholder.markdown(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            # st.rerun() dihapus agar tidak terjadi loop saat streaming
else:
    st.warning("⚠️ Masukkan data ke folder './data/'!")