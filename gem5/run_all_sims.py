import os

def get_cmd(compressor_name, prog_name, prog_options, num_core, arch):
    if "RISCV" in arch:
        cpu_type = "RiscvO3CPU"
    else:
        cpu_type = "X86O3CPU"

    return f"""build/{arch}/gem5.opt --outdir=benchmarks/results/baseline/{prog_name}/{compressor_name}/ configs/example/se.py \
                --cpu-type={cpu_type} \
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
                --options="{prog_options}"
            """

all_compressors = [
    'BaseCacheCompressor', 'BaseDictionaryCompressor',
    'Base64Delta8', 'Base64Delta16', 'Base64Delta32',
    'Base32Delta8', 'Base32Delta16', 'Base16Delta8',
    'CPack', 'FPC', 'FPCD', 'FrequentValuesCompressor', 'MultiCompressor',
    'PerfectCompressor', 'RepeatedQwordsCompressor', 'ZeroCompressor']

core_amnt = [1, 2, 4]
prog_names = ["FFT", "LU", "RADIX"]
prog_options = ["-m16", "-n512", "-n1048576"]

arch = "RISCV" # or "X86"

i = 0
for idx, prog in enumerate(prog_names):
    for core_val in core_amnt:
        for compressor in all_compressors:
            print(f"running compressor={compressor}, prog={prog}, core_val={core_val}, arch={arch}") 
            options = f"-p{core_val} {prog_options[idx]}"
            cmd = get_cmd(compressor, prog, options, core_val, arch)
            os.system(cmd)
            i += 1
            print(f"FINISHED iteration {i}\n\n\n\n\n")

print("DONE")
