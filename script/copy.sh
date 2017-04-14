function coping ()
{
    source_wav_dir=${1}
    target_wav_dir=${2}
    file_list=${3}
    source_type=${4}
    target_type=${5}

    if [ ! -d ${source_wav_dir} ]; then

        echo "ERROR: the source file dir is not exist"
    fi

    mkdir -p ${target_wav_dir}

    for x in `cat ${file_list}`; do
        
        file_dir=`dirname ${target_wav_dir}/${x}.${target_type}`
        mkdir -p $file_dir
        cp ${source_wav_dir}/${x}.${source_type} ${target_wav_dir}/${x}.${target_type}

    done
}

