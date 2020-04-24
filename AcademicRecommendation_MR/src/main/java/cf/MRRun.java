package cf;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;

import java.io.IOException;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;

public class MRRun {

	public static void main(String[] args) throws IOException {
		Configuration conf = new Configuration();
		conf.set("mapreduce.app-submission.corss-paltform", "true");
		//本地跑
		conf.set("mapreduce.framework.name", "local");
		//集群跑
		//conf.set("mapreduce.framework.name", "yarn");

		// 上传数据集到集群上，不管是否集群跑
		FileSystem fs = FileSystem.get(URI.create("hdfs://mycluster"),conf);
        // 数据集及MR结果都在dataset下
		// fs.copyFromLocalFile(".../AcademicRecommendation_MR/data/dataset/input/","/cf_dlutir/input/");

		//所有mr的输入和输出目录定义在map集合中，保存在hdfs中
		Map<String, String> paths = new HashMap<String, String>();
		paths.put("Step1Input", "/cf_dlutir/input/");
		paths.put("Step1Output", "/cf_dlutir/output/step1");
		//fs.copyToLocalFile(...)

		paths.put("Step2Input", paths.get("Step1Output"));
		paths.put("Step2Output", "/cf_dlutir/output/step2");
        //fs.copyToLocalFile(...)

		paths.put("Step3Input", paths.get("Step2Output"));
		paths.put("Step3Output", "/cf_dlutir/output/step3");
        //fs.copyToLocalFile(...)

		paths.put("Step4Input1", paths.get("Step2Output"));
		paths.put("Step4Input2", paths.get("Step3Output"));
		paths.put("Step4Output", "/cf_dlutir/output/step4");
        //fs.copyToLocalFile(...)

		paths.put("Step5Input", paths.get("Step4Output"));
		paths.put("Step5Output", "/cf_dlutir/output/step5");
        //fs.copyToLocalFile(...)

		paths.put("Step6Input", paths.get("Step5Output"));
		paths.put("Step6Output", "/cf_dlutir/output/step6");
        //fs.copyToLocalFile(...)



		MR1.run(conf, paths);
		MR2.run(conf, paths);
		MR3.run(conf, paths);
		MR4.run(conf, paths);
		MR5.run(conf, paths);
		MR6.run(conf, paths);
	}

}
