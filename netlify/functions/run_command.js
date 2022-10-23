var exec = require('child_process').exec;

export const handler = async () => {
    await new Promise((resolve, reject) => {
        exec('ls -la',
            function (error, stdout, stderr) {
                console.log('stdout: ' + stdout);
                console.log('stderr: ' + stderr);
                if (error !== null) {
                    console.log('exec error: ' + error);
                    return reject(error);
                }
                resolve();
            }
        );
    });
    return {
      statusCode: 200,
      body: JSON.stringify({
        message: 'Server is now runnning!',
      }),
    }
}
