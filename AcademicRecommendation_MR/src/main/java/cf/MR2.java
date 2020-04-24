package cf;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

/**
 按学者分组，计算所有主题词出现的组合列表，得到学者对主题词的使用次数得分矩阵
	u1	i1001:1,
	u2	i1001:1,i1002:1,
	u11	i1003:1,
	u21	i266:1,
	u24	i64:1,i218:1,i185:1,
	u26	i276:1,i201:1,i348:1,i321:1,i136:1,
 */
class  MR2 {

	
	static void run(Configuration config, Map<String, String> paths){
		try {
			FileSystem fs =FileSystem.get(config);
			Job job =Job.getInstance(config);
			job.setJobName("step2");
			job.setJarByClass(StartRun.class);
			job.setMapperClass(Step2_Mapper.class);
			job.setReducerClass(Step2_Reducer.class);
			job.setMapOutputKeyClass(Text.class);
			job.setMapOutputValueClass(Text.class);

			FileInputFormat.addInputPath(job, new Path(paths.get("Step2Input")));
			Path outpath=new Path(paths.get("Step2Output"));
			if(fs.exists(outpath)){
				fs.delete(outpath,true);
			}
			FileOutputFormat.setOutputPath(job, outpath);

			boolean f= job.waitForCompletion(true);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	 static class Step2_Mapper extends Mapper<LongWritable, Text, Text, Text>{

		 //如果使用：学者+主题词同时作为输出key，更优
		 //item	user	score
		protected void map(LongWritable key, Text value,
				Context context)
				throws IOException, InterruptedException {
			String[]  tokens=value.toString().split("\\t");
			//或者 String[] tokens = Pattern.compile("[\t]").split(value.toString());
			String item=tokens[1];
			String user=tokens[0];
			String action =tokens[2];
			Text k= new Text(user);

			int rv = Integer.parseInt(action);
			Text v =new Text(item+":"+ rv);
			context.write(k, v);
			//user    item:score
		}
	}
	
	 
	 static class Step2_Reducer extends Reducer<Text, Text, Text, Text>{

			protected void reduce(Text key, Iterable<Text> i,
					Context context)
					throws IOException, InterruptedException {
				Map<String, Integer> r =new HashMap<String, Integer>();
				//user
				// i1:1
				// i2:2
				// i3:4
				for(Text value :i){
					String[] vs =value.toString().split(":");
					String item=vs[0];
					int action=Integer.parseInt(vs[1]);

					r.put(item,action);
				}
				StringBuilder sb =new StringBuilder();
				for(Entry<String, Integer> entry :r.entrySet() ){
					sb.append(entry.getKey()).append(":").append(entry.getValue()).append(",");
				}
				
				context.write(key,new Text(sb.toString()));
			}
		}
}
