import os

def get_cmd(compressor_name, prog_name, num_core, arch):
    return f"""build/{arch}/gem5.opt --outdir=benchmarks/results/baseline/{prog_name}/{compressor_name}/ configs/example/se.py \
                --cpu-type=RiscvO3CPU \
                --cpu-clock=3GHz \
                --cacheline_size=64 \
                --caches \
                --l1i_size=32kB \
                --l1i_assoc=8 \
                --l1d_size=32kB \
                --l1d_assoc=8 \
                --num-cpus={num_core} \
                --l2cache \
                --l2_size=2MB \
                --l2_assoc=16 \
                --l3cache \
                --l3_size=6MB \
                --l3_assoc=24 \
                --l3_tags="CompressedTags" \
                --l3_compressor="{compressor_name}" \
                --cmd=benchmarks/{arch}/{prog_name} \
                --options="-p2 -m16"
            """

all_compressors = [
    'BaseCacheCompressor', 'BaseDictionaryCompressor',
    'Base64Delta8', 'Base64Delta16', 'Base64Delta32',
    'Base32Delta8', 'Base32Delta16', 'Base16Delta8',
    'CPack', 'FPC', 'FPCD', 'FrequentValuesCompressor', 'MultiCompressor',
    'PerfectCompressor', 'RepeatedQwordsCompressor', 'ZeroCompressor']

core_amnt = [1, 2, 4]
prog_names = ["FFT", "LU", "RADIX"]

arch = "RISCV" # or "X86"

for prog in prog_names:
    for core_val in core_amnt:
        for compressor in all_compressors:
            print(f"running compressor={compressor}, prog={prog}, core_val={core_val}, arch={arch}") 
            cmd = get_cmd(compressor, prog, core_val, arch)
            os.system(cmd)
            print("FINISHED RUN\n\n\n\n\n")

print("DONE")
