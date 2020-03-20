const util=require('util')

console.log('Loading logger')

const LOGLEVEL=process.env.LOGLEVEL;

const logLevels={
    DEBUG:10,
    INFO:5,
    WARN:1
}

let logLevel=1;

if(LOGLEVEL in logLevels){
    logLevel=logLevels[LOGLEVEL];
    console.log(util.format('LOGLEVEL = %s',LOGLEVEL));
}else{
    console.log('LOGLEVEL not set, default to WARN');
}

const formatter=(level,message)=>util.format('%s - %s - %s - %s', 
        level, require.main.filename,new Date(Date.now()).toISOString(),message)

console.debug=(x)=>{
    if(logLevel>=logLevels.DEBUG){
        console.log(formatter('DEBUG',x));
    }
}

console.info=(x)=>{
    if(logLevel>=logLevels.INFO){
        console.log(formatter('INFO',x));
    }
}

console.warn=(x)=>{
    if(logLevel>=logLevels.WARN){
        console.log(formatter('WARN',x));
    }
}

console.error=(x)=>{
    console.log(formatter('ERROR',x));
}

module.exports=console;
